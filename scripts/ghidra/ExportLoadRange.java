// Export at most 4096 load-module bytes, with optional non-mutating decode.
//@author N0zoM1z0
//@category TH05

import ghidra.app.script.GhidraScript;
import ghidra.app.util.PseudoDisassembler;
import ghidra.app.util.PseudoInstruction;
import ghidra.program.database.mem.FileBytes;
import ghidra.program.model.address.Address;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.mem.MemoryBlockSourceInfo;

import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;

public class ExportLoadRange extends GhidraScript
{
    private static String hex(byte[] bytes)
    {
        StringBuilder result = new StringBuilder(bytes.length * 2);
        for (byte value : bytes)
            result.append(String.format("%02x", Byte.toUnsignedInt(value)));
        return result.toString();
    }

    private Address[] resolve(FileBytes file, long fileOffset, int length,
                              long loadOffset, long loadSegment) throws Exception
    {
        Address[] addresses = new Address[length];
        for (MemoryBlock block : currentProgram.getMemory().getBlocks())
        {
            if (!block.isInitialized() || !block.isLoaded())
                continue;
            for (MemoryBlockSourceInfo source : block.getSourceInfos())
            {
                if (source.getFileBytes().isEmpty() ||
                    !source.getFileBytes().get().equals(file))
                    continue;
                long sourceOffset = source.getFileBytesOffset();
                if (sourceOffset < 0)
                    continue;
                long start = Math.max(fileOffset, sourceOffset);
                long end = Math.min(fileOffset + length, sourceOffset + source.getLength());
                for (long offset = start; offset < end; ++offset)
                {
                    int index = Math.toIntExact(offset - fileOffset);
                    if (addresses[index] != null)
                        throw new IllegalStateException("range has multiple loaded file mappings");
                    Address address = source.getMinAddress().add(offset - sourceOffset);
                    if (address.getOffset() != (loadSegment << 4) + loadOffset + index)
                        throw new IllegalStateException("mapping disagrees with explicit load segment");
                    addresses[index] = address;
                }
            }
        }
        for (Address address : addresses)
            if (address == null)
                throw new IllegalStateException("range is not completely file-backed and loaded");
        return addresses;
    }

    @Override
    protected void run() throws Exception
    {
        String[] args = getScriptArgs();
        if (args.length != 7)
            throw new IllegalArgumentException(
                "usage: ExportLoadRange.java OUTPUT LOAD_OFFSET LENGTH LOAD_SEGMENT HEADER_SIZE bytes|disassemble NONCE");
        Path output = Path.of(args[0]);
        long offset = Long.decode(args[1]);
        int length = Integer.decode(args[2]);
        long segment = Long.decode(args[3]);
        long header = Long.decode(args[4]);
        boolean decode = args[5].equals("disassemble");
        if (offset < 0 || length < 1 || length > 4096 || segment < 0 || segment > 0xffff ||
            header < 0 || !(decode || args[5].equals("bytes")))
            throw new IllegalArgumentException("invalid bounded range");
        List<FileBytes> files = currentProgram.getMemory().getAllFileBytes();
        if (files.size() != 1)
            throw new IllegalStateException("expected one original FileBytes carrier");
        FileBytes file = files.get(0);
        long fileOffset = Math.addExact(header, offset);
        if (Math.addExact(fileOffset, length) > file.getSize())
            throw new IllegalStateException("range exceeds original file bytes");
        Address[] addresses = resolve(file, fileOffset, length, offset, segment);
        byte[] raw = new byte[length];
        if (file.getOriginalBytes(fileOffset, raw) != length)
            throw new IllegalStateException("incomplete original FileBytes read");
        byte[] memory = new byte[length];
        for (int index = 0; index < length; ++index)
            memory[index] = currentProgram.getMemory().getByte(addresses[index]);
        Files.createDirectories(output);
        Files.write(output.resolve("range-filebytes.bin"), raw);
        Files.write(output.resolve("range-memory.bin"), memory);
        int decoded = 0;
        if (decode)
        {
            // This API decodes one instruction from our bounded byte array and
            // never changes the database or follows branch/call destinations.
            PseudoDisassembler disassembler = new PseudoDisassembler(currentProgram);
            try (BufferedWriter listing = Files.newBufferedWriter(
                    output.resolve("range-disassembly.tsv"), StandardCharsets.UTF_8))
            {
                listing.write("load_offset\tphysical_linear\tdatabase_address\trelocated_bytes\tinstruction\n");
                while (decoded < length)
                {
                    monitor.checkCancelled();
                    byte[] window = Arrays.copyOfRange(memory, decoded, Math.min(length, decoded + 15));
                    PseudoInstruction instruction;
                    try
                    {
                        instruction = disassembler.disassemble(addresses[decoded], window);
                    }
                    catch (Exception error)
                    {
                        listing.write("# undecoded at load offset 0x" +
                            Long.toHexString(offset + decoded) + ": " +
                            error.getClass().getSimpleName() + "\n");
                        break;
                    }
                    if (instruction == null || instruction.getLength() < 1 ||
                        instruction.getLength() > length - decoded)
                    {
                        listing.write("# undecoded or incomplete instruction at load offset 0x" +
                            Long.toHexString(offset + decoded) + "\n");
                        break;
                    }
                    int size = instruction.getLength();
                    listing.write(String.format("0x%x\t0x%x\t%s\t%s\t%s%n",
                        offset + decoded, (segment << 4) + offset + decoded, addresses[decoded],
                        hex(Arrays.copyOfRange(memory, decoded, decoded + size)), instruction));
                    decoded += size;
                }
            }
        }
        if (!decode)
            Files.deleteIfExists(output.resolve("range-disassembly.tsv"));
        String metadata = "export_nonce=" + args[6] + "\nload_segment=" + segment + "\nload_module_offset=" + offset +
            "\nlength=" + length + "\nsource_file_offset=" + fileOffset +
            "\nphysical_linear=" + ((segment << 4) + offset) +
            "\ndatabase_address=" + addresses[0] +
            "\ndisassembly_requested=" + decode + "\ndecoded_bytes=" + decoded +
            "\ndisassembly_complete=" + (decode && decoded == length) +
            "\nview=relocation-applied-memory\n";
        Files.writeString(output.resolve("range.properties"), metadata, StandardCharsets.UTF_8);
        println("Bounded range exported: " + length + " bytes at load module +0x" +
            Long.toHexString(offset) + ", load segment 0x" + Long.toHexString(segment));
    }
}

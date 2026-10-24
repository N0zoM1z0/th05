// Natural TH05 Music Room candidate, adapted from ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th02/op/m_music.cpp, GAME=5.
// UTF-8 owner; stage CP932 explicitly. The 30-byte DS-copy helper is foreign.
#pragma option -zCOP_MUSIC_SUFFIX_TEXT -zPop_01
#include <dos.h>
#include "src/op/music/music.hpp"
#include "src/op/main/strings.hpp"
#include "src/op/music/titles.hpp"
#pragma codeseg OP_MUSIC_PREFIX_TEXT op_01



int game_sel = (GAME_COUNT - 1);
const int TRACK_COUNT[GAME_COUNT] = { 14, 18, 24, 28, 23 };

// Colors
// ------
// The Music Room only redraws text whenever it changes, but fully redraws the
// B plane on every frame - first by blitting [nopoly_B], then by drawing the
// polygons on top. This places the following constraints on text colors:
// 1) Colors 0 or 1 can't be used, because those don't include any of the bits
//    that can stay constant between frames.
// 2) The hardware palette colors should be identical regardless of the state
//    of the lowest bit to make the text show up on top of the polygons. That
//    is, if a color is 5 *or* 6, hardware colors 5 *and* 6 should be
//    identical. (TH04 and TH05 rely on this.)
// 3) TH02, TH03, and TH04 populate [nopoly_B] *after* they've blitted the
//    constant tracklist, thereby including all of the text pixels in the B
//    plane. TH02 and TH03 also update [nopoly_B] with the B plane from VRAM
//    every time they blit a new comment. This allows the tracklist (TH04)
//    and/or comment colors (TH02/TH03/TH04) to simply be odd, even if 2) would
//    not apply. In that case, that lowest/least significant bit will always be
//    set when blitting back [nopoly_B], and the polygons can't affect it.
//    Together with the other constant color bits, the text then appears on top
//    of the polygons, and in the defined color. (TH02 and TH03 rely on this.)

static const vc_t COL_TRACKLIST_SELECTED = ((GAME >= 4) ? 3 : V_WHITE);
static const vc_t COL_TRACKLIST          = ((GAME >= 4) ? 5 : 3);
static const vc_t COL_CMT_TRACK          = ((GAME >= 4) ? 7 : V_WHITE);
static const vc_t COL_CMT_COMMENT        = ((GAME >= 4) ? 7 : 13);
// ------

// Coordinates
// -----------

static const screen_x_t TRACKLIST_LEFT = ((GAME == 5) ? 12 : 16);
static const int TRACKLIST_VISIBLE_COUNT = 12;

static const screen_y_t TRACKLIST_TOP = 96;
static const pixel_t TRACKLIST_H = (TRACKLIST_VISIBLE_COUNT * GLYPH_H);

static const screen_y_t LABEL_GAME_TOP = 32;
static const screen_y_t LABEL_UP_TOP = (TRACKLIST_TOP - GLYPH_H);
static const screen_y_t LABEL_DOWN_TOP = (TRACKLIST_TOP + TRACKLIST_H);

static const pixel_t CMT_LINE_W = (CMT_LINE_LENGTH * GLYPH_HALF_W);
static const vram_byte_amount_t CMT_LINE_VRAM_W = (CMT_LINE_W / BYTE_DOTS);
static const pixel_t CMT_COMMENT_H = (CMT_COMMENT_LINES * GLYPH_H);

static const screen_x_t CMT_TITLE_LEFT = (
	/**/ (GAME >= 3)  ? (RES_X - GLYPH_FULL_W - CMT_LINE_W) :
	/*   (GAME == 2) */ ((RES_X / 2) - (CMT_LINE_W / 2))
);
static const screen_y_t CMT_TITLE_TOP = ((GAME == 5) ? 32 : 64);
static const screen_x_t CMT_TITLE_RIGHT = (CMT_TITLE_LEFT + CMT_LINE_W);
static const screen_y_t CMT_TITLE_BOTTOM = (CMT_TITLE_TOP + GLYPH_H);

static const screen_x_t CMT_COMMENT_LEFT = (RES_X - GLYPH_FULL_W - CMT_LINE_W);
static const screen_y_t CMT_COMMENT_TOP = (PIANO_BOTTOM + 8);
static const screen_x_t CMT_COMMENT_RIGHT = (CMT_COMMENT_LEFT + CMT_LINE_W);
static const screen_x_t CMT_COMMENT_BOTTOM = (CMT_COMMENT_TOP + CMT_COMMENT_H);
// -----------

// ZUN bloat
static int8_t unused[104];

// Polygon state
// -------------


static const unsigned int POLYGON_COUNT = 16;

// ZUN quirk: This has to be intentional.
static const unsigned int POLYGONS_RENDERED = (
	(GAME == 5) ? (POLYGON_COUNT - 2) : POLYGON_COUNT
);

bool polygons_initialized = false;

// ZUN bloat: Could have been local to polygons_update_and_render().
static screen_point_t points[10];

static polygon_point_t center[POLYGON_COUNT];
static polygon_point_t velocity[POLYGON_COUNT];
static unsigned char angle[POLYGON_COUNT];
static unsigned char angle_speed[POLYGON_COUNT];
// -------------

// Selection state
// ---------------

uint8_t music_sel;
page_t music_page_accessed;
// The initial comment is displayed immediately, without a fade-in animation.
bool cmt_shown_initial;
static int8_t unused_byte; // ZUN bloat
// ---------------

// Backgrounds
// -----------

// Persistent intended contents of the B plane, without any polygons drawn on
// top of it.
dots8_t __seg* nopoly_B;

// ZUN bloat: Unused in TH04 and TH05 which use the bgimage system for that,
// but still present in the binary.
Planar<dots8_t far *> cmt_bg;
// -----------

cmt_line_t cmt[CMT_LINES];

// TH05 selection state
// --------------------

int track_id_at_top;
int track_playing;
int track_count_cur;
// --------------------

typedef char th05_music_comment_block_is_400[(sizeof(cmt) == 400) ? 1 : -1];
typedef char th05_music_point_scratch_is_40[(sizeof(points) == 40) ? 1 : -1];
typedef char th05_music_centers_are_64[(sizeof(center) == 64) ? 1 : -1];
typedef char th05_music_velocities_are_64[(sizeof(velocity) == 64) ? 1 : -1];
typedef char th05_music_angles_are_16[(sizeof(angle) == 16) ? 1 : -1];
typedef char th05_music_angle_speeds_are_16[(sizeof(angle_speed) == 16) ? 1 : -1];
typedef char th05_music_choices_are_600[(sizeof(MUSIC_CHOICES) == 600) ? 1 : -1];
typedef char th05_music_files_are_600[(sizeof(MUSIC_FILES) == 600) ? 1 : -1];

void pascal near track_unput_or_put(uint8_t track_sel, bool16 put)
{
	enum {
		CURSOR_LEFT = TRACKLIST_LEFT,
		CURSOR_RIGHT = (CURSOR_LEFT + TRACKLIST_W),
		CURSOR_TOP = TRACKLIST_TOP,
		CURSOR_BOTTOM = (TRACKLIST_TOP + GLYPH_H - 1),
	};

	const shiftjis_t* choice;
	vc_t col = COL_TRACKLIST;

	// ZUN bloat: The code could have been a lot simpler if [TRACKLIST_TOP] was
	// added here rather than just before graph_putsa_fx(). Then, [top] could
	// have been a `screen_y_t`.
	pixel_t top = ((track_sel - track_id_at_top) * GLYPH_H);
	if((top < 0) || (top >= TRACKLIST_H)) {
		return;
	}
	if(put) {
		grcg_setcolor(GC_RMW, COL_TRACKLIST);
		grcg_hline(CURSOR_LEFT, CURSOR_RIGHT, (CURSOR_TOP + top));
		grcg_hline(CURSOR_LEFT, CURSOR_RIGHT, (CURSOR_BOTTOM + top));
		grcg_vline(CURSOR_LEFT, (CURSOR_TOP + top), (CURSOR_BOTTOM + top));
		grcg_vline(CURSOR_RIGHT, (CURSOR_TOP + top), (CURSOR_BOTTOM + top));
		grcg_off();
	} else {
		// ZUN bloat: Blitting [TRACKLIST_W] pixels starting at
		// [TRACKLIST_LEFT] is enough.
		bgimage_put_rect_16(0, (CURSOR_TOP + top), 320, GLYPH_H);
	}
	if(track_sel == track_playing) {
		col = COL_TRACKLIST_SELECTED;
	}

	choice = MUSIC_CHOICES[game_sel][track_sel];
	top += TRACKLIST_TOP;
	graph_putsa_fx(TRACKLIST_LEFT, top, col, choice);
}

void pascal near tracklist_put(uint8_t sel)
{
	for(int i = 0; i < (track_count_cur + 2); i++) {
		track_unput_or_put(i, (i == sel));
	}
	graph_putsa_fx(TRACKLIST_LEFT, LABEL_UP_TOP, COL_TRACKLIST, LABEL_UP);
	graph_putsa_fx(
		TRACKLIST_LEFT, LABEL_DOWN_TOP, COL_TRACKLIST, LABEL_DOWN
	);
	graph_putsa_fx(
		TRACKLIST_LEFT,
		LABEL_GAME_TOP,
		COL_TRACKLIST_SELECTED,
		LABEL_GAME[game_sel]
	);
}

void near nopoly_B_snap(void)
{
	nopoly_B = HMem<dots8_t>::alloc(PLANE_SIZE);
	for(vram_offset_t p = 0; p < PLANE_SIZE; p += int(sizeof(dots32_t))) {
		*reinterpret_cast<dots32_t far *>(nopoly_B + p) = VRAM_CHUNK(B, p, 32);
	}
}

void near nopoly_B_free(void)
{
	HMem<dots8_t>::free(nopoly_B);
}

// The original DS-switching nopoly_B_put helper remains foreign.
#pragma codeseg OP_MUSIC_SUFFIX_TEXT op_01

void pascal near polygon_build(
	screen_point_t near* points,
	screen_x_t center_x,
	space_changing_pixel_t center_y,
	pixel_t radius,
	int point_count,
	unsigned char plus_angle
)
{
	int i;

	// ZUN bloat: center_y.pixel = center_y.sp.to_pixel();
	center_y.sp.v >>= SUBPIXEL_BITS;

	for(i = 0; i < point_count; i++) {
		unsigned char point_angle = (((i << 8) / point_count) + plus_angle);
		points[i].x = polar_x(center_x, radius, point_angle);
		points[i].y = polar_y(center_y.pixel, radius, point_angle);
	}
	points[i].x = points[0].x;
	points[i].y = points[0].y;
}

#define polygon_init(i, center_y, velocity_x) { \
	center[i].x = (irand() % RES_X); \
	center[i].y.v = center_y; \
	velocity[i].x = velocity_x; \
	if(velocity[i].x == 0) { \
		velocity[i].x = 1; \
	} \
	velocity[i].y.v = (to_sp(2.0f) + TO_SP(irand() & 3)); \
	angle[i] = irand(); \
	angle_speed[i] = (0x04 - (irand() & 0x07)); \
	if(angle_speed[i] == 0x00) { \
		angle_speed[i] = 0x04; \
	} \
}

inline int polygon_vertex_count(int polygon_index) {
	return ((polygon_index / 4) + 3);
}

void near polygons_update_and_render(void)
{
	int i;
	if(!polygons_initialized) {
		for(i = 0; i < POLYGONS_RENDERED; i++) {
			polygon_init(i, (irand() % to_sp(RES_Y)), (4 - (irand() & 7)));
		}

		// ZUN quirk: This is never reset.
		polygons_initialized = true;
	}
	for(i = 0; i < POLYGONS_RENDERED; i++) {
		polygon_build(
			points,
			center[i].x,
			reinterpret_cast<space_changing_pixel_t &>(center[i].y),
			(((i & 3) * 16) + 64),
			polygon_vertex_count(i),
			angle[i]
		);
		center[i].x += velocity[i].x;
		center[i].y.v += velocity[i].y.v;
		angle[i] += angle_speed[i];
		if((center[i].x <= 0) || (center[i].x >= (RES_X - 1))) {
			velocity[i].x *= -1;
		}

		// Enough to cover the maximum possible radius of 96.
		if(center[i].y >= to_sp(RES_Y + 100.0f)) {
			polygon_init(i, to_sp(-100.0f), (8 - (irand() & 15)));
		}

		grcg_polygon_c(points, polygon_vertex_count(i));
	}
}

// ZUN bloat

void near music_update_render_and_flip(void)
{
	nopoly_B_put();
	piano_render();

	// Draw the polygons via the GRCG by setting all bits in all tile registers
	// but restricting blitting to the B plane. Technically, using the GRCG
	// wouldn't be necessary and is in fact a slower way of regularly writing
	// pixels to just the B plane, but all master.lib polygon drawing functions
	// write to VRAM using `=` (MOV) rather than `|=` (OR), and thus expect the
	// GRCG to be enabled.
	grcg_setcolor((GC_RMW | GC_B), 0xF);
	polygons_update_and_render();
	grcg_off();

	// This is the correct position for a VSync delay. frame_delay() returns
	// immediately after a VSync interrupt and at the beginning of the vertical
	// blanking interval, which is the safest point to flip pages.
	frame_delay(1);

	graph_showpage(music_page_accessed);
	music_page_accessed = (1 - music_page_accessed);
	graph_accesspage(music_page_accessed);

	// ZUN landmine: Waiting for VSync *after* flipping, however, means that we
	// almost certainly *don't* flip within the vertical blanking interval, but
	// somewhere *within* a frame while the beam is still traveling across the
	// screen. This ensures a tearing line on all but the fastest PC-98
	// systems, with the pixels above always being one frame behind.
}


void pascal near cmt_load(int track)
{
	char* FN = "_MUSIC0.TXT";

	FN[6] = ('0' + game_sel);
	file_ropen(FN);
	file_seek((track * int(sizeof(cmt))), SEEK_SET);
	file_read(cmt, sizeof(cmt));
	file_close();
	for(int i = 0; i < CMT_LINES; i++) {
		cmt[i].c[CMT_LINE_LENGTH] = '\0';
	}
}

// ZUN bloat: TH05 has the most straightforward version of this code.
#define cmt_put_macro(fx) \
	graph_putsa_fx( \
		CMT_TITLE_LEFT, CMT_TITLE_TOP, (COL_CMT_TRACK | fx), cmt[0].c \
	); \
	for(int line = 1; line < CMT_LINES; line++) { \
		if((GAME >= 4) && (cmt[line].c[0] == ';')) { \
			continue; \
		} \
		graph_putsa_fx( \
			CMT_COMMENT_LEFT, \
			((line + ((CMT_COMMENT_TOP - 1) / GLYPH_H)) * GLYPH_H), \
			(COL_CMT_COMMENT | fx), \
			cmt[line].c \
		); \
	}

void near cmt_put(void)
{
	graph_putsa_fx(CMT_TITLE_LEFT, CMT_TITLE_TOP, COL_CMT_TRACK, cmt[0].c);
	const cmt_line_t near* cmt_p = &cmt[1];
	int line = 1;
	screen_y_t top = CMT_COMMENT_TOP;
	while(line < CMT_LINES) {
		if(cmt_p->c[0] != ';') {
			graph_putsa_fx(CMT_COMMENT_LEFT, top, COL_CMT_COMMENT, cmt_p->c);
		}
		line++;
		top += GLYPH_H;
		cmt_p++;
	}
}

void near cmt_fadein_both_animate(void)
{
	int func; // ACTUAL TYPE: graph_putsa_fx_func_t
	for(func = FX_MASK; func < FX_MASK_END; func++) {
		graph_putsa_fx_func = static_cast<graph_putsa_fx_func_t>(func);
		cmt_put();	music_update_render_and_flip();
		cmt_put();	music_update_render_and_flip();
	}
	graph_putsa_fx_func = FX_WEIGHT_BOLD;
	cmt_put();	music_update_render_and_flip();
	cmt_put();
}

inline void cmt_unput(void) {
	enum {
		W = (RES_X - CMT_TITLE_LEFT), // ZUN bloat: [CMT_LINE_W] is enough.
	};
	bgimage_put_rect_16(CMT_TITLE_LEFT, CMT_TITLE_TOP, W, GLYPH_H);
	bgimage_put_rect_16(
		CMT_COMMENT_LEFT, CMT_COMMENT_TOP, W, (CMT_COMMENT_LINES * GLYPH_H)
	);
}

void near cmt_unput_both_animate(void)
{
	// ZUN bloat: Not related to unblitting.
	graph_putsa_fx_func = FX_WEIGHT_BOLD;

	cmt_unput();
	music_update_render_and_flip();
	cmt_unput();
}

void pascal near cmt_load_unput_and_put_both_animate(int track)
{
	if(cmt_shown_initial) {
		cmt_unput_both_animate();
	}
	cmt_load(track);

	// ZUN bloat: These calls are never needed. Either we're rendering the
	// first track and there's nothing to be unblitted, or we already unblitted
	// the previous track title and comment in the call above.
	// In fact, they have no effect at all, which is why TH05 can put these
	// nonsensical coordinates and ZUN never noticed anything.
	nopoly_B_put();
	bgimage_put_rect_16(
		CMT_TITLE_LEFT,
		((GAME == 5) ? 64 : CMT_TITLE_TOP),
		(RES_X - CMT_TITLE_LEFT),
		((GAME == 5) ? 256 : (CMT_LINES * GLYPH_H))
	);

	if(cmt_shown_initial) {
		cmt_fadein_both_animate();
	} else {
		cmt_shown_initial = true;
		cmt_put();
		music_update_render_and_flip();
		cmt_put();
	}

	// ZUN bloat: Redundant; music_update_render_and_flip() runs almost
	// immediately after this function on every code path, and this is the
	// first thing that function does.
	nopoly_B_put();
}

// Input wrappers
// --------------
// The Music Room is the only piece of UI that is more or less the same across
// 4 of the 5 games. Therefore, it makes sense to define these here rather than
// adding more complexity to the headers.


// Same game-specific branches as in the TH03/TH04/TH05 cutscene system, but
// with a different, much smaller effect here.
//
// ZUN quirk: After processing an input, the Music Room loop wants to prevent
// held keys from having any effect by spinning in a different loop until all
// keys have been released. However, due to the different sensing functions,
// the actual handling of held keys differs depending on the game:
//
// * TH02 and TH04 use raw input sensing functions that don't address the
//   hardware quirk documented in the `Research/HOLDKEY` example. Therefore,
//   the eventual key release scancode for a held key is not filtered and gets
//   through to [key_det], breaking the spinning loop despite the key still
//   being held.
// * In TH03 and TH05, this eventual key release scancode is accurately
//   detected and filtered. Thus, held keys truly don't have any effect, but at
//   the cost of an additional 614.4 us for every call to this function.
inline void music_input_sense(void) {
	input_reset_sense_held();
}
// --------------

void pascal near tracklist_unput_and_put_both_animate(int sel)
{
	bgimage_put_rect_16(0, LABEL_GAME_TOP, CMT_TITLE_LEFT, GLYPH_H);
	bgimage_put_rect_16(0, TRACKLIST_TOP, CMT_TITLE_LEFT, TRACKLIST_H);
	tracklist_put(sel);
	music_update_render_and_flip();
	bgimage_put_rect_16(0, LABEL_GAME_TOP, CMT_TITLE_LEFT, GLYPH_H);
	bgimage_put_rect_16(0, TRACKLIST_TOP, CMT_TITLE_LEFT, TRACKLIST_H);
	tracklist_put(sel);
}

inline void track_unput_and_put_both_animate(
	const uint8_t& sel_prev, const uint8_t& sel_new
) {
	track_unput_or_put(sel_prev, false);
	track_unput_or_put(sel_new, true);
	music_update_render_and_flip();
	track_unput_or_put(sel_prev, false);
	track_unput_or_put(sel_new, true);
}

inline void game_switch(void) {
	music_sel = 0;
	track_playing = 0;
	track_id_at_top = 0;
	track_count_cur = TRACK_COUNT[game_sel];
	tracklist_unput_and_put_both_animate(0);
	snd_kaja_func(KAJA_SONG_FADE, 32);
	cmt_load_unput_and_put_both_animate(0);
	snd_load(MUSIC_FILES[game_sel][0], SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);
}

void near musicroom_menu(void)
{
	int frame_since_last_input = 0;
	uint8_t sel_prev;
	track_id_at_top = 0;
	track_playing = 0;
	music_sel = 0;
	track_count_cur = TRACK_COUNT[game_sel];
	#define SEL_QUIT track_count_cur

	cmt_shown_initial = false;

	// ZUN bloat: The call site would have been a better place for this.
	cdg_free_all();
	text_clear();

	music_page_accessed = 1;

	palette_settone(0);
	graph_showpage(0);

	// ZUN bloat: We copy page 1 to page 0 below anyway. The hardware palette
	// is also entirely black, so no one will ever see a difference.
	graph_accesspage(0);
	graph_clear();

	graph_accesspage(1);

	pi_fullres_load_palette_apply_put_free(0, "music.pi");

	piano_setup_and_put_initial();
	nopoly_B_snap();
	bgimage_snap();
	tracklist_put(music_sel);
	graph_copy_page(0);

	graph_accesspage(1);
	graph_showpage(0);


	pfend();
	pfstart("music.dat");
	cmt_load_unput_and_put_both_animate(music_sel);

	// ZUN landmine: After all the loading and blitting, we're certainly in the
	// middle of a frame, where a sudden change to the hardware palette ensures
	// tearing.
	palette_100();

	while(1) {
		// In TH05, this loop also ignores any left or right inputs while up or down are
		// held, and vice versa.
		// ZUN bloat: None of this `goto` business would have been necessary if
		// the loop clearly defined its update and render steps. Especially
		// since it does want to render the polygon animation every frame.
		while(1) {
			music_input_sense();
			if(!key_det) {
				break;
			}
			if(frame_since_last_input >= 24) {
				if((key_det == INPUT_UP) || (key_det == INPUT_DOWN)) {
					frame_since_last_input = 20;
					break;
				}
			}
			frame_since_last_input++;
			music_update_render_and_flip();
		}
controls:
		// ZUN bloat: We already did that for this frame if we came from above,
		// but not if we came from the `goto` below.
		music_input_sense();

		if(key_det & INPUT_UP) {
			sel_prev = music_sel;
			if(music_sel > 0) {
				music_sel--;
				if(music_sel < track_id_at_top) {
					track_id_at_top = music_sel;
					tracklist_unput_and_put_both_animate(music_sel);

					// ZUN quirk: This prevents game switches via left or right , but
					// only in the very specific case of
					// 1) the cursor being at the top of the list,
					// 2) highlighting a track other than the first one of the
					//    respective game, and
					// 3) left/right being pressed simultaneously with up.
					//    In any other case, left/right are processed as expected, and
					//    override this cursor movement with a game switch.
					goto skip_processing_of_left_and_right;
				} else {
					track_unput_and_put_both_animate(sel_prev, music_sel);
				}
			} else {
				music_sel = SEL_QUIT;
				track_id_at_top = (
					SEL_QUIT - (TRACKLIST_VISIBLE_COUNT - 1)
				);
				tracklist_unput_and_put_both_animate(SEL_QUIT);
			}
		}
		if(key_det & INPUT_DOWN) {
			sel_prev = music_sel;
			if(music_sel < SEL_QUIT) {
				music_sel++;
				if(music_sel >= (track_id_at_top + TRACKLIST_VISIBLE_COUNT)) {
					track_id_at_top = (
						music_sel - (TRACKLIST_VISIBLE_COUNT - 1)
					);
					tracklist_unput_and_put_both_animate(music_sel);

					// Same as the quirk above, applying to the
					// corresponding very specific case of
					// 1) the cursor being at the bottom of the list,
					// 2) highlighting anything except [SEL_QUIT], and
					// 3) left/right being pressed simultaneously with down.
					goto skip_processing_of_left_and_right;
				} else {
					track_unput_and_put_both_animate(sel_prev, music_sel);
				}
			} else {
				music_sel = 0;
				track_id_at_top = 0;
				tracklist_unput_and_put_both_animate(music_sel);
			}
		}
		if(key_det & INPUT_LEFT) {
			ring_dec(game_sel, (GAME_COUNT - 1));
			game_switch();
		} else if(key_det & INPUT_RIGHT) {
			ring_inc_ge(game_sel, GAME_COUNT);
			game_switch();
		}
	skip_processing_of_left_and_right:
		if(key_det & INPUT_SHOT || key_det & INPUT_OK) {
			if(music_sel != SEL_QUIT) {
				snd_kaja_func(KAJA_SONG_FADE, 32);
				sel_prev = track_playing;
				track_playing = music_sel;
				track_unput_and_put_both_animate(sel_prev, music_sel);
				cmt_load_unput_and_put_both_animate(music_sel);
				snd_load(MUSIC_FILES[game_sel][music_sel], SND_LOAD_SONG);
				snd_kaja_func(KAJA_SONG_PLAY, 0);
			} else {
				break;
			}
		}
		if(key_det & INPUT_CANCEL) {
			break;
		}
		if(!key_det) {
			frame_since_last_input = 0;
			music_update_render_and_flip();
			goto controls;
		}
	};

	// Wait until the player released the key that broke out of the loop
	while(1) {
		music_input_sense();
		if(!key_det) {
			break;
		}
		music_update_render_and_flip();
	}

	pfend();
	pfstart(OP_AND_END_PF_FN);
	snd_kaja_func(KAJA_SONG_FADE, 16);
	nopoly_B_free();
	graph_showpage(0);
	graph_accesspage(0);
	palette_black_out(1);
	bgimage_free();
	snd_load(BGM_MENU_MAIN_FN, SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);
}

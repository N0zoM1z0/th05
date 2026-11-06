// Copy the current bullet template into one gather circle's saved template.
#pragma option -zCGATHER_COPY_TO_TEXT -zPmain_03
#include "src/main/gather/gather.hpp"
#pragma codeseg GATHER_COPY_TO_TEXT main_03

void pascal near set_gather_template_to_bullet_template(gather_t near &gather)
{
    gather.bullet_template = bullet_template;
}

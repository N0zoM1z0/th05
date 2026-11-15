/* The VRAM page currently shown during the All Cast ending; the other one is
 * drawn to. Flipped with (ALLCAST_OPPOSITE_PAGE_SUM - page_shown). */
#ifndef TH05_MAINE_ALLCAST_PAGE_SHOWN_H
#define TH05_MAINE_ALLCAST_PAGE_SHOWN_H
#define ALLCAST_OPPOSITE_PAGE_SUM 1
#ifdef __cplusplus
extern "C" {
#endif
extern unsigned char near page_shown;
#ifdef __cplusplus
}
#endif
#endif

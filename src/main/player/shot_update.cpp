// Shot motion, homing, missile acceleration and post-hit sprite decay.
#pragma option -zCSHOT_UPDATE_TEXT -zPmain_01
#include <dos.h>
#include "src/main/player/shot_runtime.hpp"

void near shots_update(void)
{
    int i;
    shot_alive_t near *alive;
    unsigned char angle_delta;
    Shot near *shot;
    hitshot_t near *hitshot;
    shots_alive_count = 0;
    shot = shots;
    alive = shots_alive;
    for(i = 0; i < SHOT_RUNTIME_COUNT; i++, shot++) {
        if(shot->flag == F_REMOVE) {
            shot->flag = F_FREE;
        } else if(shot->flag != F_FREE) {
            if(shot->flag == F_ALIVE) {
                switch(static_cast<unsigned char>(shot->type)) {
                case ST_HOMING:
                    if(static_cast<unsigned char>(shot->age) >= 16) {
                        shot->type = ST_NORMAL;
                    }
                    if(homing_target.x.v == SHOT_SUBPIXEL_NONE) {
                        break;
                    }
                    angle_delta = shot->angle - iatan2(
                        homing_target.y.v - shot->pos.cur.y.v,
                        homing_target.x.v - shot->pos.cur.x.v);
                    if(angle_delta >= 0x80) {
                        angle_delta = (256 - angle_delta) / 4;
                        if(angle_delta < 3) {
                            shot->angle = iatan2(
                                homing_target.y.v - shot->pos.cur.y.v,
                                homing_target.x.v - shot->pos.cur.x.v);
                        } else {
                            // Angle storage is a raw byte; mutate its unsigned modulo-256 view.
                            reinterpret_cast<unsigned char near &>(shot->angle) += angle_delta;
                        }
                    } else {
                        angle_delta /= 4;
                        if(angle_delta < 3) {
                            shot->angle = iatan2(
                                homing_target.y.v - shot->pos.cur.y.v,
                                homing_target.x.v - shot->pos.cur.x.v);
                        } else {
                            reinterpret_cast<unsigned char near &>(shot->angle) -= angle_delta;
                        }
                    }
                    shot_velocity_set(&shot->pos.velocity, shot->angle);
                    break;
                case ST_MISSILE_LEFT:
                    shot->pos.velocity.x.v++;
                    goto missile_accelerate;
                case ST_MISSILE_RIGHT:
                    shot->pos.velocity.x.v--;
                case ST_MISSILE_STRAIGHT:
missile_accelerate:
                    shot->pos.velocity.y.v -= 4;
                    break;
                }
            }
            // Borrow the actual packed return only until both cache coordinates
            // are consumed; the full Motion method still returns PlayfieldPoint.
            shot->pos.update_seg1();
            if(static_cast<subpixel_t>(_AX) <= -8 * 16 ||
               static_cast<subpixel_t>(_AX) >= (384 + 8) * 16 ||
               static_cast<subpixel_t>(_DX) <= -8 * 16 ||
               static_cast<subpixel_t>(_DX) >= (368 + 8) * 16) {
                shot->flag = F_REMOVE;
            } else {
                // Finish unpacking before pointer/count updates can reuse registers.
                alive->pos.x.v = static_cast<subpixel_t>(_AX);
                alive->pos.y.v = static_cast<subpixel_t>(_DX);
                alive->shot = shot;
                alive++;
                shots_alive_count++;
                shot->age++;
            }
        }
    }
    hitshot = hitshots;
    for(i = 0; i < HITSHOT_COUNT; i++, hitshot++) {
        if(hitshot->age >= HITSHOT_FRAMES + 1) {
            hitshot->age = 0;
        }
        if(hitshot->age != 0) {
            // This returned point is needed only for the immediate signed bounds.
            hitshot->pos.update_seg1();
            if(static_cast<subpixel_t>(_AX) <= -8 * 16 ||
               static_cast<subpixel_t>(_AX) >= (384 + 8) * 16 ||
               static_cast<subpixel_t>(_DX) <= -8 * 16 ||
               static_cast<subpixel_t>(_DX) >= (368 + 8) * 16) {
                // Retain the original TH04-derived out-of-bounds sentinel.
                hitshot->age = HITSHOT_FRAMES + HITSHOT_CELS + 2;
            } else {
                hitshot->age++;
                if(hitshot->age % HITSHOT_FRAMES_PER_CEL == 1) {
                    hitshot->patnum++;
                }
            }
        }
    }
}

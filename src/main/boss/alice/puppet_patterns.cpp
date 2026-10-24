// Five complete charged puppet patterns; foreign references remain unowned.
#pragma option -zCALICE_PUP_TEXT -zPmain_03
#include "src/main/boss/alice/puppet_patterns.hpp"

bool pascal near alice_puppet_initial(AlicePuppet near &puppet)
{
    if(puppet.phase_frame == 16) {
        circles_add_shrinking(puppet.pos.cur.x, puppet.pos.cur.y);
    }
    if(puppet.phase_frame >= 32) {
        if(puppet.phase_frame < 64 && stage_frame_mod2) {
            bullet_template.patnum = 0;
            bullet_template.spawn_type = ALICE_PUPPET_NO_DECELERATE;
            bullet_template.speed.v = to_sp(2);
            bullet_template.group = BG_SINGLE;
            bullet_template.origin = puppet.pos.cur;
            bullet_template.angle = randring2_next16();
            bullet_template_tune();
            bullets_add_regular();
            puppet.patnum = 194;
        } else if(puppet.phase_frame >= 96) {
            puppet.patnum = 190;
            return true;
        }
    }
    return false;
}

bool pascal near alice_puppet_spread(AlicePuppet near &puppet)
{
    if(puppet.phase_frame == 16) {
        circles_add_shrinking(puppet.pos.cur.x, puppet.pos.cur.y);
    }
    if(puppet.phase_frame >= 32) {
        puppet.patnum = 194;
        if(puppet.phase_frame == 32) {
            bullet_template.patnum = 0;
            bullet_template.origin = puppet.pos.cur;
            bullet_template.spawn_type = ALICE_PUPPET_NO_DECELERATE;
            bullet_template.speed.v = to_sp(1.5f);
            bullet_template.group = BG_SPREAD_STACK_AIMED;
            reinterpret_cast<uint32_t &>(bullet_template.spread) =
                3UL | (18UL << 8) | (5UL << 16) | (5UL << 24);
            bullet_template.angle = 0;
            bullet_template_tune();
            bullets_add_regular();
        } else if(puppet.phase_frame >= 96) {
            puppet.patnum = 190;
            return true;
        }
    }
    return false;
}

bool pascal near alice_puppet_aimed_bursts(AlicePuppet near &puppet)
{
    if(puppet.phase_frame == 16) {
        circles_add_shrinking(puppet.pos.cur.x, puppet.pos.cur.y);
    }
    if(puppet.phase_frame >= 32) {
        puppet.patnum = 194;
        if(puppet.phase_frame < 64 && (puppet.phase_frame % 8) == 0) {
            bullet_template.patnum = 0;
            bullet_template.origin = puppet.pos.cur;
            bullet_template.spawn_type = ALICE_PUPPET_NO_DECELERATE;
            bullet_template.speed.v = to_sp(2);
            bullet_template.group = BG_SPREAD_AIMED;
            reinterpret_cast<uint16_t &>(bullet_template.spread) = 5 | (16 << 8);
            bullet_template.angle = 0;
            bullet_template_tune();
            bullets_add_regular();
        } else if(puppet.phase_frame >= 96) {
            puppet.patnum = 190;
            return true;
        }
    }
    return false;
}

bool pascal near alice_puppet_ring_bursts(AlicePuppet near &puppet)
{
    if(puppet.phase_frame == 16) {
        circles_add_shrinking(puppet.pos.cur.x, puppet.pos.cur.y);
    }
    if(puppet.phase_frame >= 32) {
        puppet.patnum = 194;
        if(puppet.phase_frame < 64 && (puppet.phase_frame % 8) == 0) {
            bullet_template.patnum = 0;
            bullet_template.origin = puppet.pos.cur;
            bullet_template.spawn_type = ALICE_PUPPET_NO_DECELERATE;
            bullet_template.speed.v = to_sp(2);
            bullet_template.group = BG_RING_AIMED;
            reinterpret_cast<uint16_t &>(bullet_template.spread) = 12 | (8 << 8);
            bullet_template.angle = 0;
            bullet_template_tune();
            bullets_add_regular();
        } else if(puppet.phase_frame >= 96) {
            puppet.patnum = 190;
            return true;
        }
    }
    return false;
}

bool pascal near alice_puppet_rings(AlicePuppet near &puppet)
{
    if(puppet.phase_frame == 16) {
        circles_add_shrinking(puppet.pos.cur.x, puppet.pos.cur.y);
    }
    if(puppet.phase_frame >= 32) {
        puppet.patnum = 194;
        if((stage_frame % 32) == 0) {
            bullet_template.patnum = 0;
            bullet_template.origin = puppet.pos.cur;
            bullet_template.spawn_type = ALICE_PUPPET_NO_DECELERATE;
            bullet_template.speed.v = to_sp(1.5f);
            bullet_template.group = BG_SPREAD_AIMED;
            reinterpret_cast<uint16_t &>(bullet_template.spread) = 7 | (12 << 8);
            bullet_template.angle = 0;
            bullet_template_tune();
            bullets_add_regular();
        }
    }
    return false;
}

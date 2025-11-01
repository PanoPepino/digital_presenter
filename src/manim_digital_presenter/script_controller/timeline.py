from ..my_imports import *

__all__ = ["play_timeline"]

def play_timeline(scene, timeline):
    """
    Enhanced Abulafia Timeline supporting both Animation objects and 
    mobject.animate syntax.
    
    Example:
        timeline = {
            0: Create(square, run_time=2),              # Animation class
            1: circle.animate.shift(UP * 2),             # animate syntax
            2: [square.animate.rotate(PI/2),             # Multiple animations
                text.animate.set_color(YELLOW)]
        }
    """
    
    previous_t = 0
    ending_time = 0
    
    for t, anims in sorted(timeline.items()):
        to_wait = t - previous_t
        if to_wait > 0:
            scene.wait(to_wait)
        previous_t = t
        
        if not isinstance(anims, Iterable):
            anims = [anims]
        
        for anim in anims:
            if hasattr(anim, 'build') and not isinstance(anim, Animation):
                # This fixes the Abulafia animation issues with inbuilt methods. 
                # The idea is to transform the method into some animation to pass it through timeline
                anim = anim.build()
            # Verify this is an Animation object
            if not isinstance(anim, Animation):
                raise TypeError(
                    f"Timeline only accepts Animation objects. "
                    f"Got {type(anim).__name__}. "
                    f"Use 'mobject.animate.method()' or Animation classes like 'Create(mobject)'."
                )
            
            # Convert animation to updater
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            
            # Handle optional sound attribute
            if hasattr(anim, "sound_to_play") and anim.sound_to_play:
                scene.add_sound(anim.sound_to_play)
                
            ending_time = max(ending_time, t + anim.run_time)
    
    if ending_time > t:
        scene.wait(ending_time - t)

class AnimationData:
    def __init__(self, frames, durations, tags):
        self.frames = frames
        self.durations = durations
        self.tags = tags

        self.current_tag = None
        self.current_frame = 0
        self.elapsed = 0
        self.playing = False
        self.frame_range = (0, len(frames) - 1)

    def set_tag(self, tag_name: str):
        for tag in self.tags:
            if tag["name"] == tag_name:
                self.frame_range = (tag["from"], tag["to"])
                self.current_frame = tag["from"]
                self.elapsed = 0
                self.current_tag = tag_name
                self.playing = True
                return
        print(f"Warning: Tag '{tag_name}' not found")

    def update(self, dt: float):
        if not self.playing:
            return
        self.elapsed += dt
        duration = self.durations[self.current_frame]
        if self.elapsed >= duration:
            self.elapsed = 0
            self.current_frame += 1
            if self.current_frame > self.frame_range[1]:
                self.current_frame = self.frame_range[0]

    def get_current_frame(self):
        return self.frames[self.current_frame]

.PHONY: film script keyframes shots music narration assemble radio-cut clean help

PYTHON ?= python3

help:
	@echo "Available commands:"
	@echo "  make film       - Run the entire AI video generation pipeline"
	@echo "  make script     - Validate storyboard.json contract"
	@echo "  make narration  - Generate Gemini Neural TTS audio"
	@echo "  make keyframes  - Generate photorealistic FLUX AI keyframes"
	@echo "  make shots      - Generate cinematic moving video shots"
	@echo "  make music      - Generate original acoustic score"
	@echo "  make assemble   - Assemble master film and dual exports"
	@echo "  make radio-cut  - Generate narration and audio radio cut"

film:
	$(PYTHON) -m pipeline.orchestrate

script:
	$(PYTHON) -m pipeline.script

narration:
	$(PYTHON) -m pipeline.narration

keyframes:
	$(PYTHON) -m pipeline.keyframes

shots:
	$(PYTHON) -m pipeline.shots

music:
	$(PYTHON) -m pipeline.music

assemble:
	$(PYTHON) -m pipeline.assemble

radio-cut:
	$(PYTHON) -m pipeline.script
	$(PYTHON) -m pipeline.narration
	$(PYTHON) -m pipeline.music
	@echo "✓ Radio cut audio ready in outputs/audio/"

clean:
	rm -rf outputs/concat_list.txt outputs/stitched_raw.mp4 outputs/video_with_endcard.mp4 outputs/end_card.mp4

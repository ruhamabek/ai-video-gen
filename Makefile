.PHONY: film script keyframes shots music narration assemble radio-cut docker-build docker-film clean help

PYTHON ?= python3
DOCKER_IMAGE ?= heritage-short:latest

help:
	@echo "Available commands:"
	@echo "  make film         - Run the entire AI video generation pipeline natively"
	@echo "  make script       - Validate storyboard.json contract"
	@echo "  make narration    - Generate neural Amharic TTS audio"
	@echo "  make keyframes    - Generate photorealistic FLUX AI keyframes"
	@echo "  make shots        - Generate cinematic moving video shots"
	@echo "  make music        - Generate original acoustic score"
	@echo "  make assemble     - Assemble master film and dual exports"
	@echo "  make radio-cut    - Generate narration and audio radio cut"
	@echo "  make docker-build - Build zero-dependency Docker container"
	@echo "  make docker-film  - Run full pipeline inside Docker container"

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

docker-build:
	docker build -t $(DOCKER_IMAGE) .

docker-film: docker-build
	docker run --rm -v $(PWD)/outputs:/app/outputs --env-file .env $(DOCKER_IMAGE)

clean:
	rm -rf outputs/concat_list.txt outputs/narration_concat.txt outputs/stitched_raw.mp4 outputs/video_with_endcard.mp4 outputs/end_card.mp4

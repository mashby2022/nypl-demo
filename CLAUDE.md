This is the instruction file we gave our AI coding agent while building this demo. It's part of the resource: read it to see how the project was steered in plain language.

# NYC Wildlife CV Project Rules

## Build & Run Commands
- Install: `pip install -r requirements.txt`
- Run Demo: `python app.py`
- Mock Data: `python mock_telemetry.py`

## Architectural Constraints
- Mapping: bird->'NATIVE: Pigeon', cat/dog->'NATIVE: Squirrel (Proxy)', mouse->'ALERT: Rat'
- Privacy: If 'person' detected, apply heavy cv2.GaussianBlur on bbox and label 'PRIVACY MASK'
- Visuals: Teal boxes for native, Crimson boxes for alerts. Solid black telemetry HUD top-left
- UI Behavior: Use cv2.waitKey(0) to step through frames manually on keypress

## Code Style
- Write compact, production-grade Python.
- Skip lengthy conversational explanations in the terminal output. Just execute.

# Room-as-Data Architecture: Unified State Projection for MUD and ScummVM

## 1. Overview

This specification defines a unified room state object that serves as the single source of truth for two distinct rendering projections: a text-based MUD (Multi-User Dungeon) and a ScummVM-compatible graphical scene. The architecture decouples room semantics from presentation, enabling dynamic, sensor-aware environments that mutate in real time across both interfaces.

## 2. Canonical JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://example.com/room.schema.json",
  "title": "RoomState",
  "type": "object",
  "required": ["id", "description", "exits"],
  "properties": {
    "id": { "type": "string", "pattern": "^[a-zA-Z0-9_-]+$" },
    "description": { "type": "string", "minLength": 1, "maxLength": 2000 },
    "background_prompt": { 
      "type": "string", 
      "description": "Stable Diffusion prompt for scene generation" 
    },
    "camera_source": { 
      "type": ["string", "null"], 
      "format": "uri", 
      "description": "Optional RTSP stream URL for live video overlay" 
    },
    "npc_models": {
      "type": "array",
      "items": { 
        "type": "string", 
        "description": "Ollama model name (e.g., 'llama3', 'mistral')" 
      },
      "default": []
    },
    "exits": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "Map of exit direction to target room ID"
    },
    "sensor_inputs": {
      "type": "object",
      "properties": {
        "imu": { "type": ["object", "null"], "description": "Inertial measurement data (accel, gyro, mag)" },
        "ais": { "type": ["object", "null"], "description": "Automatic Identification System vessel data" },
        "gps": { 
          "type": ["object", "null"],
          "properties": {
            "lat": { "type": "number", "minimum": -90, "maximum": 90 },
            "lon": { "type": "number", "minimum": -180, "maximum": 180 }
          }
        }
      },
      "default": {}
    }
  }
}
```

## 3. MUD Projection (Text Serialization)

The MUD projection transforms the JSON into an interactive text description through a deterministic renderer:

### 3.1 Serialization Pipeline
1. **Description extraction**: The `description` field is emitted verbatim as the first paragraph.
2. **Dynamic sensor augmentation**: If `sensor_inputs.gps` exists, append a coordinate line: `"You detect your position: 37.7749° N, 122.4194° W"`. IMU data (e.g., tilt, vibration) is converted to atmospheric text: `"The ground trembles beneath you (roll: 0.12 rad)."`
3. **NPC listing**: For each model in `npc_models`, generate a presence line: `"A shimmering presence of [model_name] watches you."` The model is loaded lazily via Ollama API for dialogue.
4. **Exit rendering**: Exits are formatted as a bracketed list: `"[n]orth → dark_cave, [e]ast → village_square"`.
5. **Camera feed hint**: If `camera_source` is non-null, append: `"A surveillance feed flickers in your mind's eye (RTSP active)."`

### 3.2 State Mutation
The MUD projection listens for JSON patches (RFC 6902). Any change to `description`, `sensor_inputs`, or `exits` triggers a re-render of the text buffer. The projection maintains a session cache to avoid re-serializing unchanged fields.

## 4. ScummVM Projection (Canvas Rendering)

The ScummVM projection renders the room as a 2D interactive scene using a custom engine plugin:

### 4.1 Rendering Pipeline
1. **Background generation**: The `background_prompt` is fed to a local Stable Diffusion instance (via API) to produce a 640×480 background image. This image is cached with an SHA-256 hash of the prompt; re-rendering occurs only on prompt change.
2. **Camera overlay**: If `camera_source` is present, the RTSP stream is decoded via FFmpeg and composited as a semi-transparent layer over the background (alpha=0.7), enabling live video in the scene.
3. **Dynamic sprites**: Each NPC model in `npc_models` is represented by a placeholder sprite (silhouette). On first interaction, the model generates a spoken line via Ollama, displayed in a speech bubble.
4. **Sensor visualization**:
   - **GPS**: A minimap icon is drawn at the bottom-right corner showing coordinates.
   - **IMU**: Vibration effects (screen shake) applied if acceleration magnitude > threshold.
   - **AIS**: Vessel positions plotted as dots on a nautical chart overlay if `ais` data is present.
5. **Exits**: Clickable hotspots are rendered as glowing arrows at screen edges, mapped to exit directions.

###

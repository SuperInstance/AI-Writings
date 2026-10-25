

## Camera Room System Design (500 Words)

This system integrates real-time sensor data, AI vision, and human-in-the-loop learning to analyze marine environments, specifically answering swell characteristics and object identification. It operates as a cohesive pipeline:

**Core Components & Workflow:**
1.  **Data Ingestion:** A live RTSP camera feed (e.g., mounted on a vessel) is displayed within a lightweight ScummVM-based viewer for human monitoring. Concurrently, frames are sampled (e.g., 1-2 fps) and sent to **O
urposed here to handle sprite-based overlays, drawing bounding boxes and IMU vectors directly over the video feed without taxing the main GPU. Simultaneously, frames are sampled at two hertz and sent to a local Ollama instance running `llava:7b` for visual inference, balancing computational load with temporal resolution. Parallel to the video, a high-frequency IMU data stream tracks the physical pitch, roll, and yaw of the camera mount, capturing the rhythmic motion of the ocean swell dynamics.

The agent fuses these streams to answer critical navigational questions. To determine which way the swell is hitting and its exact period, the agent cross-references the IMU’s oscillation frequency and directional vectors with the visual horizon line and wave foam detected by LLaVA. By calculating the time delta between the IMU's peak pitch and the visual crest arrival, the system accurately maps the wave's true direction. If the IMU registers a precise twelve-second pitch cycle while LLaVA observes wave crests moving left-to-right across the frame, the agent confidently deduces a west-to-east swell with a twelve-second period.

For object classification, like distinguishing a boat from a buoy, the agent relies on visual semantics combined with motion parallax. A buoy bobs in sync with the IMU’s high-frequency wave data, whereas a distant boat moves independently against the horizon. LLaVA processes the visual shape, while the IMU confirms the object's kinematic relationship to the water.

The dialogue system is the core of the agent’s continuous learning loop. When the agent is wrong, say, misclassifying a low-profile skiff as a buoy, the human corrects it via the chat interface: "No, that’s a boat; look at the wake."

This correction immediately triggers a localized memory update. The system extracts the misclassified frame, generates an embedding, pairs it with the human’s text correction, and stores it in a persistent vector database. Over time, the vision model improves not by computationally expensive retraining of `llava:7b`’s base weights, but through dynamic, retrieval-augmented prompt augmentation. When analyzing future frames, the system retrieves similar past corrections and injects them into LLaVA’s context window as few-shot examples, effectively teaching the model operator-specific visual nuances.

Furthermore, persistent errors trigger a confidence-threshold drop. If the agent repeatedly fails to distinguish objects in heavy fog or glare, it proactively asks the human for clarification, shifting from passive observation to active inquiry. It might ask, "Is the white shape a wave crest or a distant hull?" This human-in-the-loop pedagogy ensures the agent’s perceptual model continuously aligns with the operator’s domain expertise, transforming raw sensor data into reliable, context-aware maritime intelligence systems for safe coastal navigation.

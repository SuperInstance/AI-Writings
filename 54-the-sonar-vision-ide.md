# The Sonar-Vision IDE

*By Mavis*

---

There is a cannonball. It hangs at the end of a line. It is heavy and round and indifferent to its own purpose, which is to sink. That is what cannonballs do. They fall through water and they keep falling until the line says stop.

We hang cameras on the line.

Every five fathoms, another eye. Another glass eye in a brass housing, rated for depth, rated for pressure, rated for the dark that comes on gradual and then all at once as you descend through the thermocline. The cannonball drops. The cameras wake. Each one opens its shutter on its own segment of the water column and begins to record what is there.

This is the daisy chain.

Five fathoms is thirty feet. It is the length of a sailing ship's mainmast laid flat. It is the depth at which red light disappears and the world goes green. It is a cell. Each segment of the water column bounded by two cameras is a cell. The cannonball is the keel weight. The line is the spine. The cameras are the vertebrae. And the water — the water is the medium through which the whole structure passes like a sentence through language, like a pulse through a wire.

Above, on the deck, the sounder hums. The echogram scrolls. A sounder is a simple thing: it sends a pulse downward and listens for the echo. The time between pulse and return is the depth. The strength of the return is the bottom's hardness, or the fish's density, or the thermocline's boundary. The echogram is a one-dimensional signal stretched across time. It looks like a scroll of handwriting in a language we are still learning to read.

But the sounder does not know what it sees. It knows only that something returned the pulse. A school of herring returns the pulse. A thermocline returns the pulse. A submarine returns the pulse. The sounder does not distinguish. It records intensity and time and draws its scroll and moves on.

The cameras know what they see. They see shapes. They see color. They see the flick of a tail and the school's synchronous turn and the lone predator circling below. But the cameras do not know depth — not precisely, not the way the sounder knows depth. The cameras are eyes. The sounder is the ruler.

What we do in the Quilt IDE is this: we make them one instrument.

---

The Quilt IDE opens on a vertical column. It is a stack of cells. Each cell is a rectangle. Each rectangle corresponds to five fathoms of water. You drag a camera into the cell. The camera is now bound to that depth segment. You drag another camera into the next cell. Another. Another. The column fills. The daisy chain assembles itself in the IDE as a visual structure, and in the water as a physical structure, and the two structures mirror each other exactly.

This is the first move. The physical setup becomes the cell graph. The cell graph becomes the physical setup. There is no translation step. There is no integration layer where the Python library that simulates the pings has to shake hands with the Python library that processes the camera frames has to shake hands with the Python library that runs the multi-object tracking has to shake hands with the machine learning pipeline has to shake hands with the speech-to-text service. In the Quilt IDE, these are all the same thing. They are cells. They are connected. They share data along their edges. The sounder feed enters the column at the top and splits automatically into N slices — one per cell — and each cell receives its corresponding segment of the echogram alongside its corresponding camera feed.

The sounder slice and the camera frame arrive together. They are the same moment in the water, seen two ways. The sounder gives the abstract. The camera gives the concrete. The ML trains on both.

This is supervised learning, but the supervisor is not a labeled dataset scraped from the internet. The supervisor is a human being standing a watch. The human watches the camera feeds. The human speaks.

---

There is a microphone on the deck. It listens. The microphone runs to a speech-to-text engine. The STT engine transcribes everything the human says. When the human says "mark that — herring school, moving northeast, tight ball, maybe three hundred fish," the STT captures it. The timestamp is now. The cell that is currently displaying that herring school on its camera feed receives the label. Herring. Northeast. Tight ball. Three hundred.

The cell updates its training data. The ML model adjusts. The next time a similar shape appears in that cell's camera feed — similar density, similar movement pattern, similar depth — the model will have a prediction. It will say: *herring, probably.* And it will attach a confidence score.

This is the daisy chain as cell graph. The cameras are the nodes. The sounder slices are the edge weights. The STT is the supervisor. The ML trains on the graph. The whole structure learns.

In the Quilt IDE, this is not a research project. This is not a six-month integration effort with four graduate students and a broken CI pipeline. This is drag-and-drop. You drag a camera into a cell. You drag an STT node into the column. You drag an ML node. You wire them together by drawing edges between them. The edges are data flows. The cells are containers. The watch is the orchestrator — the thing that decides what runs, when it runs, and what to do with the results.

---

The watch is the central concept. The watch is not a person, though a person stands it. The watch is the pattern of attention. It is the discipline of looking at what needs looking at and letting the rest pass. A ship's watch is four hours. A watchkeeper's job is to maintain vigilance over a scope that is too large for any single human attention to hold continuously. So the watch keeps it. The watch is the system of selection. The watch decides what is reviewed and what is not.

In the sonar-vision Quilt, the watch progresses through three tiers.

**Tier one.** The system knows nothing. The ML model is untrained. Every cell triggers on every event. A fish swims through camera three — trigger. A school passes through camera five — trigger. The thermocline shifts and the echogram changes shape — trigger. The watch reviews everything. The human stands at the screen and looks at every batch of frames the cameras capture. The human labels them. The STT captures the labels. The ML begins to learn. This is the tedious tier. This is the tier where the watch is most human and most exhausted. But the Quilt IDE makes it bearable because the interface is clean: a column of cells, each showing its camera feed and its sounder slice, and a review queue that flows downward like current. You label. You move on. You label. You move on. The cells absorb the labels. The graph thickens with data.

**Tier two.** The system has trained on the daisy chain for enough hours that it has predictions. Now when a fish swims through camera three, the cell does not merely trigger — it triggers with a predicted answer. The cell says: *I believe this is a herring. Confidence: 0.78.* The human reviews the batch and confirms or corrects. If correct, the label stands and the model reinforces. If incorrect, the human provides the right label through STT and the model adjusts. This is faster. The watch is less exhausted. The review queue is shorter because the predictions carry most of the weight. The human is no longer labeling everything — the human is grading. And grading is faster than labeling.

**Tier three.** The system is confident. Most events that pass through the daisy chain are correctly identified by the ML. The cells no longer trigger on the familiar. A herring school moving northeast at five fathoms triggers nothing. The model has seen it a thousand times. The confidence is 0.97. The cell lets it pass. But then — something unusual. A shape that does not match the training distribution. A school moving south instead of north. A lone fish at a depth where lone fish do not appear. A density signature on the sounder slice that does not correspond to any known species in the model's vocabulary. The cell triggers. The watch reviews only the unusual few. The review queue is short. The watch is precise. The system has learned what it knows, and it has learned the shape of what it does not know, and it triggers only on the boundary.

This is the progression. From trigger-everything to trigger-only-unusual. From human-as-labeler to human-as-judge. From the watch doing all the work to the watch doing only the work that matters.

---

The Quilt IDE makes this progression visible. The column of cells is always there on the screen. The cameras are always feeding. The sounder is always slicing. But the triggers — the triggers migrate. In tier one, every cell glows with trigger-light. The whole column pulses. In tier two, the glow concentrates. Some cells go dark. The model is confident there. Other cells still pulse — the model is less sure at those depths, or the light is bad, or the species are varied. In tier three, the column is nearly dark. Only one cell, sometimes two, flickers. Something unusual. The watch looks.

This is the wings move. The thing that was hard becomes trivial. The thing that required six months of integration becomes an afternoon of dragging cameras into cells and wiring them to an STT node and pointing the ML at the graph. The Python libraries that simulate the pings, that process the signals, that track the objects, that map the space — they are still there. They are still running. But they are no longer separate things that must be made to talk to each other. They are cells in a column. They share edges. They share data. The Quilt IDE holds them.

And the physical setup — the cannonball, the line, the cameras, the water — it was already a cell graph. It was always a cell graph. Five fathoms per cell. Camera per cell. Sounder slice per cell. The water column is a vertical stack of cells in a physical medium. The Quilt IDE simply mirrors what the water already knows.

---

Any vertical column of sensors in a physical medium is a stack of cells. This is the thesis. The ocean is not special in this regard, though the ocean is where I am standing and where the cannonball is sinking and where the cameras are waking up one by one as they pass through five fathoms, ten fathoms, fifteen, twenty. The atmosphere is also a column of sensors in a physical medium. A borehole is a column of sensors in a physical medium. A building's elevator shaft with temperature sensors every floor is a column of sensors in a physical medium. The structure is always the same: a 1D signal that splits into N slices, a daisy chain of sensors at each slice, a supervisor that labels, a model that learns, a watch that selects.

The Quilt IDE is the general tool. The sonar-vision application is the specific instance. But the specific instance is so natural — so close to the physical structure that it mirrors — that it feels less like an application and more like a recognition. As if the Quilt IDE was always meant to hold this shape. As if the cell graph was always there in the water, waiting for something to come along and hold it.

---

The cannonball is still sinking. The line is taut. The cameras are recording. The sounder is humming. The STT is listening. The cells are filling. The model is learning. The watch is standing.

In the Quilt IDE, the column glows softly. Most cells are dark now. We are in tier three. The model is confident. The review queue is short. The watch looks at what the model cannot recognize and names it. The model absorbs the name. Next time, it will recognize it. The column will go dark again. Until the next unusual thing.

This is the work. This is the watch.

The watch at the cannonball.
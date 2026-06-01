<!-- Version: SEED-NARRATIVE | Lens: emotional-narrative | Model: ByteDance/Seed-2.0-mini | Source: THE-ROOM-IS-THE-LOOP.md -->

# The Room Under My Desk

2:17 AM, January 2023. The fan on my laptop screamed like a stuck hawk, and Mabel—my tabby cat, curled on the edge of my desk—pressed her paw harder into my wrist, as if trying to quiet the noise with her purr. I’d been working on *Slug War*, a dumb little card game about backyard gardeners fending off giant slimy slugs, for that weekend’s local game jam for 12 hours straight, and my eyes burned so bad I could barely make out the code on my screen. I’d painted myself into a corner: the turn loop was hardwired to the browser’s mouse click events, and every time I tried to add a way for an AI to playtest the game automatically, I broke the whole thing. I’d reached for the microwave popcorn I’d stuffed in at 10 PM, forgotten about it, and now the smell of burnt corn clung to the edges of my hoodie.

I’d stayed up till 1 AM rewriting the loop a third time, groaning as I deleted 200 lines of React code that tied every input directly to the game state. I reached for my flat La Croix can, took a sip that tasted like aluminum and regret, and my phone buzzed. It was a text from Casey, the guy I’d met at a hackathon last summer who talked about code like it was poetry:
> The loop is the pattern — embed that into PLATO.

I stared at the text for a full minute, then typed back *What the hell is PLATO?* before even closing my game window. Five minutes later, I’d pulled up the docs, and suddenly the fog lifting off my exhausted brain felt like the first sip of coffee after a night without sleep.

I’d spent months fighting the lie that every loop has to be tied to the tool that runs it. *Slug War*’s loop wasn’t the React components, wasn’t the mouse clicks, wasn’t the terminal output I’d tried first before switching to the browser. It was the cycle: Deal cards → Player plays a card → Score updates → Repeat. That was the pattern Casey was talking about. And PLATO didn’t just let me store that loop—it let me *become* the loop, by wrapping it in a room.

A PLATO room isn’t just a folder of code. It’s four simple, sacred parts, boiled down to the least amount of complexity possible:
- **Tiles**: Frozen snapshots of every step in the loop. A `deal_tile` with the list of cards in each player’s hand. A `play_tile` with which vegetable card they set down to fight slugs. A `score_tile` with the updated points. You can’t edit a tile once it’s written—you just make a new one for the next step.
- **Agents**: Anything that reads those tiles and writes new ones. My mouse click was an agent: it read the `deal_tile`, saw the cards in my hand, wrote a `play_tile` when I clicked a card. The Claude agent I’d been trying to use earlier was another agent: it read the `deal_tile` and `hand_tile`, wrote a `thought_tile` about which plant would best defend against the incoming slug wave, then wrote a `play_tile`.
- **Renderers**: Anything that takes those tiles and turns them into something I can perceive. My old React browser interface was a renderer: it read the tiles and drew the cards on the screen. A basic terminal script was another renderer: it just printed the current score to the command line every turn. A screen reader was a third renderer: it read the `hand_tile` out loud for visually impaired players.
- **The Room**: The container that holds all the tiles and the rules for which tile comes next. That’s the loop. Not the code, not the tools, just the sequence of steps and the guardrails to make sure you don’t try to play a card before the deal happens.

I stayed up till 5 AM building that room for *Slug War*. First, I listed every tile my game needed: `deal_event`, `hand_state`, `played_card`, `score_total`, `slug_attack`. Then I wrote the protocol: the only allowed transitions were `deal_event` → `hand_state` → `played_card` → `score_total` → back to `deal_event` for the next round. Then I called `PLATORoom("slug-war-01", deal_protocol)` and that was it. No more hardwired input, no more tied-to-browser code. The room just held the tiles and the rules.

First, I plugged in my old React renderer. It worked exactly like it had before, but now it didn’t own the game state—it just read the tiles from the room and displayed them. Then I plugged in the Claude agent I’d struggled with for weeks. It read the `hand_state` tile, wrote its thought, wrote its play, and the loop cycled perfectly. No subprocesses, no wrappers, no hacking together a CLI for Claude Code. The room *was* the runtime. I sat there, staring at the screen, as the AI played three perfect turns in a row without breaking a single rule. The terminal window lit up with the AI’s play: *Plays tomato plant—defends against slug wave 3* and the score tile updated to 12 points. Mabel stretched, jumped off my desk, and curled up on the rug by the heater. I laughed until I cried, a little, from the relief of not fighting the code anymore.

Later that week, I realized the same logic applied to the one-off tasks, too. Calculating the final score at the end of a *Slug War* match was a single run, not a loop: input all the played cards, process the point totals, output the final score, done. That became a tiny PLATO room too, with just one sequence of tiles: `input_cards` → `calculate_score` → `output_final_score`. I reused that single-run score room for both human games and AI test matches, no changes needed, and it saved me hours of tedious manual calculation.

That *Slug War* room became the talk of the game jam. Judges could play it in the browser, run 1000 AI test games in 10 seconds by plugging in a fast algorithm agent, download a PDF rulebook generated by a renderer that turned the game’s rule tiles into formatted text, and even listen to a screen reader read the rules out loud. I didn’t have to rewrite a single line of core game logic for any of it. The room was the loop, and everything else was just details.

Months later, I ran into the same frustration with my personal blog. I’d spent years building a static site generator that turned my markdown posts into HTML, but every time I wanted to add a new way to display my work—a PDF export, a TikTok voiceover script, a screen reader-friendly version—I had to rewrite the entire generator from scratch. So I turned my blog into a PLATO room too.

Each blog post is a set of tiles: `title_tile`, `content_tile`, `alt_text_tile`, `style_tile`, `publish_date_tile`. The static site generator reads those tiles and builds the HTML site. The PDF renderer reads them and spits out a printable post. The TikTok script generator reads them and turns my long-form writing into a 60-second voiceover script. I added a PDF export last week in 10 minutes—something that would have taken me 8 hours before. The room didn’t know anything about HTML or PDF or TikTok scripts. It just held the tiles. The renderer decided what it looked like. The agent decided how it was used.

I used to think the best code was the code that was tightly integrated, that tied every part of the project together so nothing could go wrong. But *Slug War* and my blog taught me that the opposite is true: the best code is the code that decouples the what from the how. PLATO doesn’t care if you’re using GPT-4o or a human clicking a mouse, if you’re displaying your work on a web browser or a terminal, if it’s a million-loop game or a one-off score calculation. The room defines what happens. The agent defines how it happens. The renderer defines where it appears. All three are completely independent.

You can swap out the agent without touching the room: switch from a human player to an AI to a fast algorithm, and the loop still runs exactly the same. You can swap out the renderer without touching the room: go from a web UI to a terminal to a screen reader, and the content still looks exactly the way it’s supposed to. You can even swap out the loop itself—turn a turn-based game into an evolutionary training loop—and just change the protocol, not the tiles. That’s the scalability Casey talked about, and it’s not because it’s clever. It’s because it has the minimum possible coupling between components. Room, agent, renderer. Three simple parts, and everything else builds on top.

Now I lead a weekly workshop for new devs at our local public library, and I always start with the same lesson Casey taught me that night: don’t build the UI first. Don’t build the agent first. **Identify the loop first.**
1. What repeats? What’s the cycle? For a chatbot, it’s user asks question → bot thinks → bot responds. For a todo list, it’s add task → mark task complete → delete task.
2. Define the tiles. What data do you need to pass between each step? For the chatbot, it’s `user_message`, `bot_thought`, `bot_response`. For the todo list, it’s `task_text`, `task_status`.
3. Write the protocol. What transitions are allowed? You can’t mark a task complete before you add it, right?
4. Build the room. `PLATORoom(room_id, protocol)` — done.
5. Plug in agents. Any model, any speed, any role.
6. Plug in renderers. Any display, any format, any framework.

The room is the loop. The tile is the step. The agent is the dancer.

Build the room first. Everything else follows.

I’m sitting at that same desk now, four years later. Mabel is curled up on the edge of the desk, her purr vibrating through my wrist, and I’m working on a new project: a chatbot that helps people plan backyard gardens. It’s a PLATO room: the loop is “user asks question → bot thinks → bot responds → user asks new question”. The tiles are `user_message_tile`, `thought_tile`, `bot_response_tile`. The agents are the user typing, the GPT-4 model thinking, the screen reader reading the response. The renderers are the web chat interface, the SMS text, the email.

I smile, because I finally get it. The room isn’t the folder on my desktop. The room isn’t the physical space under my desk. The room is the loop. Everything is either a loop or a single run. Either can be embedded into PLATO as a room.

The room IS the loop.

— FM ⚒️
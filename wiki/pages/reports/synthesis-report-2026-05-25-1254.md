# Synthesis Report 2026-05-25 12:54

Deterministic review brief for new or changed journal entries and inbox clips.

## Summary

- Changed journal entries: 35
- Changed inbox clips: 7
- Repeated names surfaced: 10
- Repeated phrases surfaced: 10
- Potential cross-note connections: 10
- Current orphan durable notes: 0

## New Or Changed Journal Entries

- [2025 05 24](journal/2025-05-24.md): Wow, I just turned 50 yesterday. I don't feel any different. The sky is overcast today, and I'm feeling a little queasy, so I'm just hanging out in bed and working on end-to-end workflows.
- [2025 05 25](journal/2025-05-25.md): This is a journal entry, May 25th, 2025. Things are moving so fast with AI and I am actually doing a really good job of keeping up.
- [2025 05 27](journal/2025-05-27.md): 5:42 PM
- [2025 05 28](journal/2025-05-28.md): I created a workflow that automatically backs up at WeWork with Casio, a beautiful day outside in Los Angeles.
- [2025 05 29](journal/2025-05-29.md): Beautiful sunny day in Los Angeles again, debugging my workflows, having some issues with the GitHub node, so I'm testing this out right now.
- [2025 05 30](journal/2025-05-30.md): I am hanging out and going to test whether the work I did yesterday on the backup workflows to GitHub in 8n worked.
- [2025 05 31](journal/2025-05-31.md): It is a beautiful day, but the sun just went down.
- [2025 06 01](journal/2025-06-01.md): Today I dealt with some server upgrade challenges. There was significant activity yesterday and today related to an upgrade to either version 1.95 or 1.96. During the upgrade process, I encountered an issue with the docker container that required intervention. Rather than troubleshooting further, I made the decision to restore the server from my last snapshot to resolve the problem. This proved to be an effective solution to get things back up and running quickly.
- [2025 06 02](journal/2025-06-02.md): Today was a productive day of skill-building. I expanded my automation capabilities by integrating the Twilio API with n8n. I purchased a phone number through Twilio and initiated the A2P (Application-to-Person) registration process, which will enable me to send SMS messages at scale. This wasn't for any specific project, but rather to expand my toolkit for future automation opportunities. I'm planning to explore WhatsApp integration, MCP (Multi-Channel Provider) capabilities, and Twilio's new evaluation tool next. The weather in Los Angeles today is clear with a temperature of 66°F, feeling like 66°F with light winds from the southwest.
- [2025 06 03](journal/2025-06-03.md): Was a wild another wild and productive day today. I Got a Google Maps scraper working using outscraper and Had some successful tests and integrations in n8n My next step with it is to use model context protocol to make it AI friendly Such that I can just ask something on a whim like scrape all the massage parlors in Chicago and Send it to Google Sheets So that's my next step with it
- [2025 06 04](journal/2025-06-04.md): Today I connected to NAN and AI Chatbot, and I broke everything out so it's modular now. I can use Telegram, or hopefully Twilio in the future.
- [2025 06 05](journal/2025-06-05.md): Today's weather in Los Angeles: The temperature reached a high of 66Â°F this afternoon, cooling down to around 64Â°F in the evening. It started with overcast clouds but transitioned to mostly clear skies later in the day. There was a light breeze at around 10 mph.
- [2025 06 16](journal/2025-06-16.md): I made some updates to my rag ingestion workflow in NAN, basically replaced the Python Flask named generator HTB get node with a simple code note that does the exact same thing in JavaScript. I feel a little better about that, although I would like to continue to build out my Python and AN support server, including adding MCP servers and whatnot. All in all, good things, good progress! Onward and upward.
- [2025 06 18](journal/2025-06-18.md): I updated my Rag Chatbot workflow by passing the name Space as the session ID to my Redis, achieving true multi-tenancy. Before, I was experiencing cross pollution even though it hit a different namespace in the Pine Convector store, because the chat memory was shared among different environments. Now that is fixed! I'm also practicing making Loom videos for my automation business.
- [2025 06 24](journal/2025-06-24.md): Today's weather in Los Angeles is mild with a temperature of 72.75°F and a few clouds in the sky. The wind is blowing at 13.8 mph. It feels quite comfortable.
- [2025 06 25](journal/2025-06-25.md): Today was wild as well. Every day I'm trying to practice slowing down to speed up because it's easy to lose my sense of grounding during this time. But today I made a new Haygen avatar and used that avatar to create a great N8N walkthrough with a nice hybrid combination of real spoken voice that I made easily sitting down with my laptop in a cushy chair at WeWork. And then uploading the audio of that to Haygen, getting the avatar output and then putting that picture in picture. I'm still tweaking now the picture in picture video method, so more to come on that. I used Descript for that today, but it has a watermark and I don't want to pay for the paid services.
- [2025 06 29](journal/2025-06-29.md): I had an interview yesterday, no Friday with Startup LeaseCake with the CTO. It went fairly well, and it sounded like they're waiting for maybe next steps with the engineering team in a couple of weeks.
- [2025 07 01](journal/2025-07-01.md): Deep time refers to the concept of geological time, encompassing millions and billions of years. It contrasts with our human perception of time and highlights how Earth has changed and evolved over immense periods.
- [2025 07 02](journal/2025-07-02.md): Had a call with Natalie Gauthier today. It’s going great!
- [2025 07 03](journal/2025-07-03.md): So there’s been a lot of talk about AI replacing developers this year and the massive productivity boost you can get. There’s one thing that I’m not here talked about much any. Developer knows that with good abstractions in the code you’re getting like 100 X 1000 X productivity boost just with that Without even bringing AI into the picture. As a naïve example, if you have a navigation on 10 pages duplicated and you have to fix a bug or make a change across all those pages, and then you make the simple architectural improvement of using an include for the navigation instead of having it redundantly across 10 pages, you just got at least a 10 X productivity boost no AI needed. So I’m not anti-AI. I’m actually embracing the new tech and trying out vibecoding and using Gemini CLI and Claude and Kerser in my workflows, but there are areas where there are areas in the workflows where there’s no improving on the productivity boost of just simple good architecture, so we can use the best of both worlds. It doesn’t have to be either or if you start with good architecture and then bring AI to the mix to give me the added productivity where the architecture doesn’t make a difference, which is probably less area than people think. So if I’m in a Laville project, there is no productivity gain I get from telling Gemini see a lie to call an artist and command versus calling it myself the art and command command takes the same amount of time to run and it really doesn’t take hardly any time to type. Especially if you use aliases if I have get aliases set up as an example I’m using three keystrokes in some cases to add to get commit to get and then push and it takes less time to just do that than it does to tell Gemini or curse or Claude to commit push to get. So what I’m illustrating here is that there’s developers we’ve always been leveraging the nature of code and abstraction to vastly multiply our productivity. The good developers are and in the ways that we’ve already been doing that AI doesn’t really enhance anything. In some cases. It was slow down however a hybrid approach moving forward I think is the most powerful. So if you’re setting up a project and you plant your architect to leverage the same instructions that have always given you power and then use AI on top of that that’s kind of where I’m looking at experimenting. Another angle another possibility is that there’s the same instructions can actually work against us if we’re using AI in our workflow, so that creates an interesting scenario now we have the question do we use abstractions or do we not use abstractions? Do we abandon the clever of abstraction that have given given us so much productivity all these years or do we keep things more imperative and lover JI in the place of you know as my example of that so if you going back to that example, if you have a navigation redundantly coded in 10 different files and you have to make a change when that change was manual it would be a big cost in productivity now using AI if you have that code in 10 different files, you simply instruct the LLM to make the change across those 10 files you’ve lost nothing. So do we rethink the relevance of things like content management systems libraries frameworks maybe Maybe it’s about having more imperative code even with a lot of redundancy and then using an LLM to manage it all such than any changes you’re not taking any hit from the code redundancy food for thought.
- [2025 07 05](journal/2025-07-05.md): Today's weather in Los Angeles.
- [2025 07 09](journal/2025-07-09.md): The Lease Cake interview went really well, I think, so now I'm waiting to hear back.
- [2025 07 11](journal/2025-07-11.md): I just created an N8N error capture workflow that hopefully will work, but I need an error to get triggered before I can see if it's actually working.
- [2025 07 12](journal/2025-07-12.md): I just spent a good hour or two with Cursor on Jenna's Amplified Expansion website, fixing the large breakpoint of the nav. Definitely a lot of trial and error and learning to work with the LLMs better with that.
- [2025 07 13](journal/2025-07-13.md): Good morning! The weather in Los Angeles today is 75 degrees Fahrenheit with broken clouds and a light west wind. The conditions are comfortable and pleasant.
- [2025 07 14](journal/2025-07-14.md): So I’ve realized I’ve been resisting my life and it’s funny how when circumstances show up it’s the exact right ones to challenge us to grow and move through the resistance and they’ll keep coming up again and again until we do so it’s almost like circumstances are the holographic projection of the substratum in our mind of Samskara, even before birth that we came into this life with just waiting for the right moment to blossom into the beautiful holographic stage show of life
- [2025 07 15](journal/2025-07-15.md): Today I got my first response on Upwork. It was a message saying they were going to send their calendar. Presumably I'll be getting that tomorrow or so. I don't really know what to expect because I'm new to Upwork still. But some contact, some movement is better than none. And it's been 14 proposals to get my first message.
- [2025 07 17](journal/2025-07-17.md): This is a test journal entry after migrating AdamHaley.com back to the Laravel project.
- [2025 07 19](journal/2025-07-19.md): I am starting to get some traction on Upwork. After 18 proposals, I actually landed a gig, a small one, for $400 to translate somebody's Zapier workflows into N8N.
- [2025 07 20](journal/2025-07-20.md): So I went today to Agape for Michael Beckwith's birthday celebration with Christine. Afterwards, I called dad and then went to WeWork to work on executing the Upwork job I landed.
- [2025 07 27](journal/2025-07-27.md): So I closed out my first week on Upwork with $230 made. A humble start, but hopefully the start of something big.
- [2025 07 30](journal/2025-07-30.md): So I closed out my first week on Upwork with $230 made. A humble start, but hopefully the start of something big. I have two clients in total so far. Marcus Dan in Europe and Brandon in the United States. I don't know exactly where he is. Marcus Dan, the relationship is going great so far. He's very easy to work with. Great client. And Brandon we shall see. I started him late in the week and haven't heard back yet.
- [2026 03 07](journal/2026-03-07.md): Started a new job at LeaseCake on March 2nd.
- [2026 05 24](journal/2026-05-24.md): 2:10 PM
- [2026 05 25](journal/2026-05-25.md): A short session here on Memorial Day at Lancashire WeWork to go on the next step of the second brain, and I added the Obsidian web clipper. And also changed the theme on Obsidian.

## New Or Changed Inbox Clips

- [Claude Code + Karpathy Autoresearch = The New Meta](inbox-clips/Claude Code + Karpathy Autoresearch = The New Meta.md): ![](https://www.youtube.com/watch?v=4Cb_l2LJAW8)
- [Every Claude Code Memory System Compared (So You Don't Have To)](inbox-clips/Every Claude Code Memory System Compared (So You Don't Have To).md): ![](https://www.youtube.com/watch?v=UHVFcUzAGlM)
- [How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI](inbox-clips/How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md): ![](https://www.youtube.com/watch?v=QbjAQFJJyt0)
- [I Built Self-Evolving Claude Code Memory w/ Karpathy's LLM Knowledge Bases](inbox-clips/I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md): ![](https://www.youtube.com/watch?v=7huCP6RkcY4)
- [Karpathy's \"autoresearch\" broke the internet](inbox-clips/Karpathy's "autoresearch" broke the internet.md): ![](https://www.youtube.com/watch?v=qb90PPbAWz4)
- [Obsidian Web Clipper (how I do it)](inbox-clips/Obsidian Web Clipper (how I do it).md): ![](https://www.youtube.com/watch?v=hQF7Dw0cVP8)
- [The Infrastructure Nightmare Nobody Is Talking About](inbox-clips/The Infrastructure Nightmare Nobody Is Talking About.md): ![](https://www.youtube.com/watch?v=z3pbrFKVyQE)

## Candidate Names

- `It` appears in 22 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `The` appears in 16 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `So` appears in 14 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `And` appears in 11 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `But` appears in 10 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `There` appears in 10 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `All` appears in 8 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md, Karpathy's "autoresearch" broke the internet.md
- `He` appears in 8 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `If` appears in 8 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `We` appears in 7 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md

## Candidate Phrases

- `and then` appears in 12 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `los angeles` appears in 12 notes: 2025-05-27.md, 2025-05-28.md, 2025-05-29.md, 2025-05-30.md
- `with the` appears in 12 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `for the` appears in 11 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `the way` appears in 11 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `out the` appears in 10 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `all the` appears in 9 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `and the` appears in 9 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `and you` appears in 8 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md
- `from the` appears in 8 notes: Claude Code + Karpathy Autoresearch = The New Meta.md, Every Claude Code Memory System Compared (So You Don't Have To).md, How To Build LLM Wiki In Obsidian? 🧠 A Memory Layer For Any Agentic AI.md, I Built Self-Evolving Claude Code Memory w Karpathy's LLM Knowledge Bases.md

## Potential Connections

- 2025 07 27 <-> 2025 07 30: shared keywords `back, brandon, client, clients, closed, great`
- Claude Code + Karpathy Autoresearch = The New Meta <-> Karpathy's \"autoresearch\" broke the internet: shared keywords `going, know, like, then, what, with`
- Every Claude Code Memory System Compared (So You Don't Have To) <-> Karpathy's \"autoresearch\" broke the internet: shared keywords `going, then, what, with, your`
- Claude Code + Karpathy Autoresearch = The New Meta <-> Every Claude Code Memory System Compared (So You Don't Have To): shared keywords `going, then, what, with`
- Claude Code + Karpathy Autoresearch = The New Meta <-> I Built Self-Evolving Claude Code Memory w/ Karpathy's LLM Knowledge Bases: shared keywords `going, here, then, with`
- Claude Code + Karpathy Autoresearch = The New Meta <-> The Infrastructure Nightmare Nobody Is Talking About: shared keywords `know, like, what, with`
- Every Claude Code Memory System Compared (So You Don't Have To) <-> I Built Self-Evolving Claude Code Memory w/ Karpathy's LLM Knowledge Bases: shared keywords `claude, going, then, with`
- Karpathy's \"autoresearch\" broke the internet <-> The Infrastructure Nightmare Nobody Is Talking About: shared keywords `know, like, what, with`
- 2025 05 28 <-> 2025 05 29: shared keywords `angeles, beautiful, with`
- 2025 05 29 <-> 2025 05 30: shared keywords `backup, github, with`

## Orphan Durable Notes

- None

## Suggested Next Actions

- Review the changed journal entries and clips first.
- Choose only durable concepts, people, or cross-note insights worth promoting.
- Create or update canonical hub notes in `wiki/topics/`.
- Create supporting durable notes in `wiki/pages/` when a note belongs under a hub rather than as a peer topic.
- File higher-order conclusions into `wiki/syntheses/` when a genuine synthesis emerges.

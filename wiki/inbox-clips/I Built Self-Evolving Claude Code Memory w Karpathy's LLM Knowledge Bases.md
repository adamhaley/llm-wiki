---
title: "I Built Self-Evolving Claude Code Memory w/ Karpathy's LLM Knowledge Bases"
source: "https://www.youtube.com/watch?v=7huCP6RkcY4&t=87s"
author:
  - "[[Cole Medin]]"
published: 2026-04-06
created: 2026-05-25
description: "Andrej Karpathy posted about using LLMs to build personal knowledge bases - raw articles go in, an LLM compiles them into an interconnected wiki, and health checks keep everything consistent. It went"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=7huCP6RkcY4)

Andrej Karpathy posted about using LLMs to build personal knowledge bases - raw articles go in, an LLM compiles them into an interconnected wiki, and health checks keep everything consistent. It went massively viral.  
  
But here's the thing: the most valuable raw data isn't external articles. It's your own conversations with your agents.  
  
Every time you work with Claude Code, you make decisions, discover gotchas, learn patterns, and build up context that vanishes when the session ends or the context window compacts. What if instead of losing all of that, every conversation automatically compiled into a structured knowledge base that gets smarter over time?  
  
That's what I built and in this video I'll show you how to use it!  
  
\~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
\- Try InsForge - the open source platform that gives your coding agent a database, auth, storage, AI model routing, and hosting all in one. Free to get started, use code InsForgePromo for a free month of Pro:  
https://insforge.dev/  
  
\~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
\- If you're interested in building your own AI second brain to save yourself hours every week, check out the Dynamous community and the new 4 hour second brain bootcamp:  
https://dynamous.ai/second-brain-bootcamp  
  
\- Karpathy inspired Claude Code memory system repo:  
https://github.com/coleam00/claude-memory-compiler  
  
\- Karpathy's original Tweet:  
https://x.com/karpathy/thread/2039805659525644595  
  
\- Gist to build your own Karpathy LLM knowledge base:  
https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f  
  
\~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
0:00 Karpathy LLM Knowledge Bases  
2:32 How it Works  
6:01 Data Flow and Architecture  
8:40 My Claude Code Memory System  
9:19 InsForge  
10:43 Setting Up the System  
11:04 Obsidian Setup and Vault Configuration  
12:16 Claude Code Hooks  
16:51 The Compounding Knowledge Loop  
18:35 Outro  
  
\~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
Join me as I push the limits of what is possible with AI. I'll be uploading videos weekly - at least every Wednesday at 7:00 PM CDT!

## Transcript

### Karpathy LLM Knowledge Bases

**0:00** · Let's face it, every week you and I are playing the game what's the latest and greatest in the AI space, right? It changes every single week and right now everyone is focused on LLM knowledge bases, which originated from this tweet from Andrej Karpathy and there are a lot of really cool ideas here that I want to get into with you and I built my own memory system on top of this I think you're really going to like. It's simple but super effective. So, more on that in a bit but let's get into a bit of context here.

**0:27** · So, Karpathy starts by saying something I'm finding very useful recently is using LLMs to build personal knowledge bases for various topics of research interest. So, taking external information, bringing it into our own system and organizing it in the best way for agents to query. And this is a big use case for AI second brains right now, which is something I've been focusing on a lot recently and I love seeing that he's using Obsidian as a core part of his stack. I always call it my canvas for working with things with my second brain. So, cool to see that.

**0:58** · And he really gives us his entire playbook here. It's nice and simple. So, he talks about how he brings in information, data ingestion, how he views it, how he queries it, how he formats it, health checks that he's built in as well. And so, I want to cover this entire architecture here and that'll guide us into the custom solution that I've built on top. I'm excited to show you this cuz here's the thing, this entire thing that he's presenting is working with external data, which there are a lot of use cases for that. But what I've built here is working with internal data.

**1:29** · So, giving Claude code a memory that evolves with your code base. So, basing the whole LLM knowledge base on our conversations with our coding agent or second brain instead of bringing in external data. But I've structured everything in exactly the same way. All of the optimizations for how we index and create systems for our agent to explore the information. It's really cool. So, let's get into the infrastructure and then I'll show you how you can use to evolve any code base.

**1:57** · And yes, Claude Code does already have a memory system built in and there are open source solutions out there already for Claude Code long-term memory, but I wanted to build this specifically because I am following everything Karpathy laid out here to a T just for internal instead of external information. It's a lot simpler than other approaches already out there and I would argue even more effective.

**2:20** · You'll see what I mean when we get into it. So, something really interesting that he says at the top here is he's spending more of his tokens with his agents manipulating knowledge like markdown and Obsidian instead of manipulating code. But, he works with knowledge in a very similar way that we work with code. That brings us to the compiler analogy. This is the simplest way to explain everything that he's built in the system here because the way that we're handling knowledge is very similar to how we take source code all the way into a final application for the end user to run with a compiler. And so, let let's take it from the top here.

### How it Works

**2:53** · So, we start with our source code, which for the case of our LLM personal knowledge bases, it's our articles, papers, anything that we are finding online that we want to bring into our system. So, I'll go to the Obsidian vault because this is what Karpathy uses. This is what I use for my AI second brain. We have the raw folder here. This is the entry point into our system where we'll dump anything, articles, papers, transcripts, everything just as raw markdown. And then we'll take that and move it into the compiler stage.

**3:22** · This is where we have a large language model process all this raw information. So, creating summaries, linking documents together, just generally figuring out how to structure our knowledge. And for the system that Karpathy has designed here for the compiler, we do actually have scripts. We have code that takes our raw information and gives it to an LLM to produce the wiki here. So, that brings us to the next step. The compiler goes to the executable. This is what we run or in the case of our personal knowledge base, this is what we query. So, he calls it a wiki.

**3:54** · This is where we have our compiled articles, everything produced from the large language model, and we have the backlinks. We are connecting pieces of knowledge together.

**4:03** · So, going back to Obsidian again, we have our graph view. This is one of the coolest parts of Obsidian, where we can see how our different pieces of knowledge, our different markdown documents, are connected together through backlinks. And this is powerful because it gives our agent the ability to traverse through the graph, to search better, and even connect different pieces of knowledge together to give us a more comprehensive answer. So, this is what we run. This is what we search. But before we actually get to the final step with the runtime, we also have a test suite.

**4:34** · To continue with the analogy of code here, we are performing linting. He calls it linting over our documents. So, we're finding gaps where maybe we need to do more research, any kind of stale data, things that maybe we have in our raw folder that aren't actually in our wiki yet, and we need to take care of that discrepancy, any kind of broken links, like if we have one document linking to another that doesn't exist, we're going to take care of all of that.

**4:59** · And so, we're even going so far in this system as to making sure that our data has integrity. And that's pretty important. We want to have an accurate personal knowledge base. And then finally, we get into the last step here, where we are running queries, right?

**5:13** · This is the runtime, where we are taking advantage of our wiki, having our agent search through it to find information for what we are currently working on.

**5:22** · And the really interesting thing here is Karpathy said, "I thought I had to reach for fancy rag, but the large language model has been pretty good about auto maintaining index files." And so, one of the most important files in this entire setup, within the wiki, we have the index. So, this file describes to the agent, "Here are all of the different folders and resources that you have access to." So, it uses this as a starting point, so we don't even have to do fancy rag. The agent can just navigate through all the files that we have as marked down in our Obsidian vault.

**5:52** · It doesn't have to do any semantic search. There's no vector database here. It's nice and simple.

**5:57** · It's one of the beauties of this strategy that really drew me to build on top of it. Okay, so let's now go from the compiler analogy to the exact data flow. Think this will really take it home for you. Then we'll get into my implementation that I built on top. I'll talk about how it relates to all these ideas here. So, okay. We start with our external information. And Karpathy specifically calls out the Obsidian web clipper. It's a really neat extension to Obsidian that allows us to very easily take anything from the internet and bring it directly into our vault or in this case right into our raw folder.

### Data Flow and Architecture

**6:29** · The source of truth, like we talked about earlier, the unprocessed markdown. Then we feed that into the large language model to create our wiki for us. And so, I've built up a simple example here for demonstration. My raw folder just has some different articles on AI topics.

**6:47** · And then within the wiki, this is what is processed. This is what our agent actually queries. We have this concepts folder, and this is where we tie everything together. We're taking ideas, concepts out of our raw documents. And we also have connections, how different things are relating together. And then of course we have the index. This is the main file that we want our agent to always have access to so that it has a high-level idea of where it's going to start looking based on our question. And then the last thing that we have here is the agents.md. So, this is like global rules for your coding agent, right?

**7:17** · And so, really what we do in our global rules here is we're describing the entire system for LLM knowledge bases, so that the agent understands, here's where my information comes from, here's the compiled version that I'm going to search, here is the index and the log file, right? Like the entire system we explain to the agent, so it has that meta reasoning. It understands what it's been dropped in. When you start a new session with your second brain or coding agent, whatever it is.

**7:46** · And the best part is, if you want to build this entire LLM knowledge base system for yourself, all you need to do is send this prompt into your coding agent. It could not be simpler. So, this came directly from Karpathy. He had a follow tweet where he linked to this. This is essentially a PRD, right? a product requirement document that outlines everything we have to build for you to include this system in your own coding agent or second brain. And so, you just prompt this in, no other context, and it's just going to one-shot the whole thing for you.

**8:17** · And that's what I built into my version as well. If you look at the readme here for the quick start, you don't even have to clone the repo yourself. You just send this prompt into your Claude code. Clone it and then set up everything with the Claude code hooks, everything that I have to make this LLM personal knowledge base, but for internal information in instead of external. So, inspired by the entire architecture we just covered here, but that's the key difference is now this is giving Claude code a memory that evolves with your code base.

### My Claude Code Memory System

**8:47** · So, instead of taking things from the internet, we are going to automatically capture session logs with hooks. And so, session logs are kind of like the raw folder where we're just putting in our conversations, and then we're going to use the Claude agent SDK behind the scenes to automatically extract everything into structured cross-reference knowledge articles. So, your coding agent, like you can do this per code base. It's going to get smarter and smarter over time because it remembers the decisions you've made and how you evolved your project.

**9:18** · The sponsor of today's video is Inspo Forge. Inspo Forge is an open-source platform that gives your coding agent everything it needs to ship full stack apps. Think if you had Vercel, Superbase, and Open Router all in one platform. So, we have a database, we've got authentication, storage. We can route to 50 different large language models. We have hosting as well. It is everything you need and we give our agent the ability to manage all of this through a CLI and an agent skill. And take a look at this.

### InsForge

**9:46** · It literally takes less than 5 minutes to install the In Forge CLI and skill on any code base and then I can go into Claude Code and prompt it to create an application. So here I'll have it make both a back end and a front end and I'm specifically asking it to use In Forge to create my database table, set up authentication, to host it as well. Once it goes through this entire process here, then we end with a hosted application. What I'm showing you right here is a live URL and I have authentication set up so I can even demo this here. I created an account off camera. I'll sign in.

**10:17** · We have access to our database behind the scenes. So this is not just local storage, a hosted application, live database. I can even use an AI model to recommend a task for me here. So showing off the AI part of In Forge as well. We have got everything running and we didn't have to configure anything ourselves. In Forge is open source and free to get started. Plus you can use promo code In Forge promo for a free month of pro. I'll have a link in the description. So seriously, you should just try this right now.

### Setting Up the System

**10:44** · Open up Claude Code in whatever code base you're currently working on, your second brain, open Claude, whatever and just send in this prompt. It'll immediately level up the long-term memory for your coding agent when it's working on that project specifically. We're building up lessons and takeaways for this code base. And so I have the repository cloned locally.

### Obsidian Setup and Vault Configuration

**11:04** · I'm just going to work within it directly to give you an example here, but you're going to use this prompt to bring it into wherever you are already working. And so you don't have to do this, but I would recommend starting with an Obsidian vault. It's our canvas to view all of the memories in the whole wiki that we create with Claude Code.

**11:21** · And so you'll open a folder as a vault.

**11:23** · Once you have Obsidian installed, it's free and super easy to install.

**11:27** · So I'll open here and you just have to give it a path to where wherever you have the code base that you've brought in this system. So, I'll just select this folder right here. That'll create a brand new Obsidian vault. I usually like to make it look nice as well when I first create a vault. So, I'll go into the settings in the bottom left. I'll go to appearance and then manage to select a theme. They've got a lot of really awesome ones. Obsidian night is my favorite. So, I will click install and use. And then I usually like to switch to the dark theme as well. There we go.

**11:54** · Now it looks like the other vault I showed you earlier for a demo. And so, this is where we're going to manage the daily logs. I'll talk about this in a second. And then also this is our wiki equivalent where we have our index. I mean, everything this is exactly what Karpathy has set up with the concepts and connections. Everything that we use a large language model to process from our raw input. So, this entire system is only driven by Claude code hooks. So, that's the beautifully simple part about it.

### Claude Code Hooks

**12:22** · That's why all you have to do is send in this prompt to get everything set up for your code base where you run Claude code. We don't have to install anything else. We don't have to set up any integrations. And so, going to our settings.json, this is where you always define your hooks for Claude code. I want to at least at a high level show you how everything works here. I think it'll really click for you. So, we start with a session start hook. And so, this is going to run whenever we start a new Claude code session. And all we're doing with this simple Python script is loading in the agents.md.

**12:52** · We covered this earlier. That's so our Claude code understands the system that we put in it. And then it's also loading in if we go into the knowledge, this is our wiki equivalent. We're loading in our index.md. You've already seen this as well. This is our actively maintained list of files so our agent can query more efficiently.

**13:12** · And so, whenever we begin a new Claude code session, it has both of those things already. And so, now I can ask a question. Just for a demo purposes, I have a knowledge base already built up for a project. And so, I'm asking something that it wouldn't really know by itself without having to do a deep analysis in the code base. But, right here, it's just going to rely directly on what we have in our knowledge base.

**13:33** · Take a look at that. Based on your knowledge base, here are the key things to watch out for. Then, some technical details you don't have to cover here, but then it calls out the specific KB articles that it referenced in order to get us this answer. And so, the index told it where to point. It ran some queries we'll talk about in a little bit, and it pulled things from our knowledge. And so, again, we have the equivalent of our raw folder with our daily logs. This is where we're going to capture summaries of every single conversation with Claude code. I'll show you how we do that with the other hooks in a second.

**14:04** · So, daily logs, that's our raw equivalent. And then, we have our wiki. This is where we have the things that are better formatted, linked together. We have the whole graph view here in Obsidian. This is what our agent is searching through. And I know this is a really basic example here, but just like think for a second how powerful this actually is. If I ask this question without this whole system built in, it would have had to look through the git log, and even that might not have had the lessons for what to watch out for.

**14:32** · It would have had to spin up sub-agents to look through the code base, which would be painfully slow, especially if the code base was bigger. But, since we're maintaining takeaways from all of our conversations with Claude code, I was able to get this answer in like 10 seconds. You saw it happen live. And so, the other really powerful part of this entire system is the other two hooks. We have a pre-compact and a session end.

**14:53** · And they're both actually doing a very similar thing. Whenever we're about to lose context, either through closing off a session or doing memory compaction, we want to send the latest messages from Claude code into another large language model to process and create the summary.

**15:11** · And that summary is what we're going to put in the daily log file. So, like this is the summary from one conversation, you know, decisions that were made, lessons that were learned, action items, and then we go on to the next session.

**15:21** · We have a very standard format here handling every single Claude code session.

**15:26** · And the way that this works is this hook, actually both of these hooks, they are going to call the Claude agent SDK under the hood. So, we have a separate Claude process running where it's just given the transcript from the conversation and it summarizes things here. So, we're doing that initial layer of data processing. And not to get too technical here, but one other really powerful part of this is we have the flush process.

**15:52** · And so, once a day, we're going to take the logs. We're going to extract the concepts and connections from them and then that's what we populate in the wiki. And then our search is going to focus here in knowledge, but then it can also look through the daily logs if we want as well. So, we have full information about everything here, lessons learned, decisions made. If you want to customize this, you can even go into the scripts here. You can go into the flush or you could go into the compile and you can actually change the prompt that we send into the Claude agent SDK under the hood.

**16:23** · So, another beautiful part about this whole setup, unlike Claude code's memory system, is you can customize this to your heart's content. And Claude code can even walk you through making the customizations because it has access to the agents.md.

**16:37** · It knows how everything works. It knows where the prompts are. It knows how the memory promotion process works. It knows where the daily logs are. So, it's very it's a very self-contained system that can improve itself. And speaking of improving itself, that's actually the last big thing that I want to cover with you. I want to talk about the compounding loop. Cuz think about this with me for a second. We always will start by asking some kind of question.

### The Compounding Knowledge Loop

**17:00** · We want to leverage our knowledge base.

**17:02** · We're going to get some kind of answer with our agent searching across many different wiki articles. So, it's extending its arm across our knowledge base, synthesizing information together, but then it's going to file that single answer. So, we're constantly connecting information between our conversations and saving that. And so our Wiki grows over time because of that. And then also all the new information coming in from all of our future Claude code sessions.

**17:27** · And so we're building up our knowledge base over time. The agent is going to be able to search through our knowledge better over time as we ask more questions. It just gets better and better and better. And we really don't have to do anything to maintain this.

**17:41** · For example, if I extend the conversation where I ask our first question here to have it do more web research, I have more takeaways. All I have to do is end the session or do a memory compaction. And then automatically, we can see that the logs are I saw this just come up here. We already have the Claude agent SDK running in the background. It can use your Anthropic subscription just like Claude code. So you don't have to set up any API key or anything. And it's automatically going to extract takeaways and put it in our daily logs. Let's actually look at this right now cuz I believe it already finished. There we go. Take a look at this.

**18:12** · So this is our session that just ran. We were exploring best practices for handling external service data. And then we have these key exchanges, lessons learned from our additional web research. We're building this up over time. It'll eventually get promoted into our Wiki here. We don't have to do anything. And the questions that we ask our agent are just going to get better and better answers over time.

### Outro

**18:35** · Very, very powerful. So there you go.

**18:37** · That is LLM knowledge bases for internal data, long-term memory for our second brains instead of external data like Karpathy's implementation. But of course, thanks to him for all of the inspiration here. And Claude code hooks is something I've been building into my second brain for a long time now. And so I recently did a 4-hour workshop in the Dynamis community where I showed everything. I actually built my second brain again from scratch.

**19:00** · And so definitely check out the Dynamis community linked in the description and pin comment if you're interested in building your own second brain on top of Claude code and the Claude agent SDK.

**19:12** · Otherwise, if you appreciate this video and you're looking forward to more things on building agents and second brains, I would really appreciate a like and a subscribe. And with that, I will see you in the next video.
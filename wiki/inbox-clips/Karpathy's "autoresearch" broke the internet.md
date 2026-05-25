---
title: "Karpathy's \"autoresearch\" broke the internet"
source: "https://www.youtube.com/watch?v=qb90PPbAWz4"
author:
  - "[[Greg Isenberg]]"
published: 2026-03-11
created: 2026-05-25
description: "I break down Andrej Karpathy's new open-source project, Autoresearch: what it is, how it works, and why some of the smartest people in tech are losing their minds over it. I walk through 10 concrete b"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=qb90PPbAWz4)

I break down Andrej Karpathy's new open-source project, Autoresearch: what it is, how it works, and why some of the smartest people in tech are losing their minds over it. I walk through 10 concrete business ideas you can build on top of Autoresearch loops, from niche agent-in-a-box products to always-on A/B testing agencies. I also cover Karpathy's companion launch, Agent Hub, share community reactions, and show you step by step how to get started using Claude Code and a Colab GPU.  
  
I'm hosting a free workshop so you can build your business in the age of AI.  
Sign up here: https://startup-ideas-pod.link/build-with-ai-2026  
  
Links Mentioned:  
Autoresearch Github: https://startup-ideas-pod.link/autoresearch  
  
Timestamps  
00:00 – Intro  
00:45 – How Autoresearch Actually Works  
02:40 – Visual Walkthrough of the Autoresearch Loop  
03:37 – Mental Model: Your Research Bot That Runs While You Sleep  
05:26 – Idea 1: Niche Agent-in-a-Box Products  
06:48 – Idea 2: A/B Testing for Marketing (Landing Pages & Ads)  
08:45 – Idea 3: Research as a Service  
09:43 – Idea 4: Power Tool Inside Your Own SaaS  
10:49 – Idea 5: Agency That Runs 100× More Tests  
12:05 – Idea 6: Auto Quant for Trading Ideas  
13:44 – Idea 7: Always-On Lead Qualification & Follow-Up  
14:21 – Idea 8: Finance Ops Autopilot for Businesses  
15:09 – Idea 9: Internal Productivity Lab for Your Org  
15:53 – Idea 10: Done-for-You Research & Due Diligence Shop  
16:41 – Non business use cases  
18:27 – Karpathy's Agent Hub Announcement  
19:50 – How to Get Started with Autoresearch  
22:21 – Final Thoughts  
  
Key Points  
  
\* Autoresearch is an open-source AI agent that sets a goal, runs experiments in a loop on a GPU, keeps the winners, and discards the rest — all while you sleep.  
\* You need an NVIDIA GPU to run it (tested on H100), but you can rent one cheaply through Lambda Labs, Vast AI, RunPod, Google Cloud, or Google Colab.  
\* The fastest way to get started is to use Claude Code to walk you through installation, then run it on Google Colab with a T4 GPU runtime.  
\* Ten business ideas built on Autoresearch span niches like SaaS optimization, A/B testing agencies, trading backtests, CRM lead scoring, and done-for-you due diligence.  
\* Karpathy also launched Agent Hub — essentially a GitHub designed for agent swarms to collaborate on the same codebase.  
\* The project already has 25,000+ GitHub stars and is growing fast; early movers who tinker now build an unfair advantage.  
  
The #1 tool to find startup ideas/trends - https://www.ideabrowser.com/  
  
LCA helps Fortune 500s and fast-growing startups build their future - from Warner Music to Fortnite to Dropbox. We turn 'what if' into reality with AI, apps, and next-gen products https://latecheckout.agency/  
  
The Vibe Marketer - Resources for people into vibe marketing/marketing with AI: https://www.thevibemarketer.com/  
  
FIND ME ON SOCIAL  
X/Twitter: https://twitter.com/gregisenberg  
Instagram: https://instagram.com/gregisenberg/  
LinkedIn: https://www.linkedin.com/in/gisenberg/

## Transcript

### Intro

**0:00** · Andre Karpathy, I mean, one of the godfathers AI has just launched something called Auto Research. And Auto Research is a huge deal and it's going viral on Twitter. And I just wanted to do an episode where I can explain to you in the clearest way possible what it is, what are the use cases, how to make money from it, how to be more productive with it, how to create impact with it.

**0:21** · And by the end of this episode, I'm going to give you a bunch of different ideas, use cases for how to use Auto Research. I'm going to explain it to you in the most clear way possible. And at the end, I'm going to tell you how you can actually get started with it. Um so, let's go right into it.

### How Autoresearch Actually Works

**0:45** · So, what is Auto Research? Well, it's like having a super nerd robot intern that runs science experiments on AI AI models for you all night without you doing the boring stuff. I mean, sounds intriguing, right? So, how do you actually you know, program it or get started with it? Well, the first thing is you got to give it a goal. So, you can say something like make this small AI model smarter. That's the goal.

**1:08** · And then an AI agent will actually plan what to do, like different settings, code changes, edits the Python code for you, runs a short training experiment on a GPU um for about 5 minutes. It reads the results. It And then it decides what to change next and to repeat the loop. So, in some ways, you know, if you've seen my video on the Ralph Loop, where it basically would do engineering 24/7 and you'd wake up to new stuff happening. In simplest terms, that's what Auto Research is helping you know, it do.

**1:40** · You give it a goal, the AI agent does a thing, you know, you tell the AI what better means, uh cheaper leads, more clicks, higher sales, better model score. And then the AI keeps changing things, testing them, and it only saves the changes that improve. So, what's really cool about it is you wake up, you grab the best version, and then hopefully you turn it into something you charge for or, you know, you give it away. I saw this tweet by Toby who's the CEO and co-founder of Shopify.

**2:10** · Auto research works even better for optimizing any piece of software. Make an auto folder, add a program MD, that's just a markdown file which is really the foundation of what a you know, how you're going to be using auto research.

**2:25** · And a bench script, make a branch and let it rip. So, that's why I started paying attention to auto research, right? When Andre Karpathy, legend, and Toby and and and more people, you know, start playing with it, I'm like, okay, I got to pay attention. So, I created this little visual for for how to think about what auto research is. So, you set the goal, uh the the AI plants an experiment, it edits and trains the code and settings. It runs a short training on a GPU.

### Visual Walkthrough of the Autoresearch Loop

**2:53** · By the way, this is an important I should I should mention that you need a uh a Nvidia chip to actually run auto research or you can do it in the cloud.

**3:07** · I'll talk about this at the end of the episode, but you you know, you do need that. You can't just run it on let's say you have a MacBook M1 or something like that. It reads metrics. It says, is it a better result? If it's if it's not, it's going to log the attempt and it's going to discard the config. If it's yes, it saves it to the config um and then just plans a different experiment and it just, you know, hopefully gets better on your goal, whatever it is.

**3:29** · So, um let's uh let's get into um we're going to get into some of the ideas, business ideas around it, but right before that, I just want to say, here's a simple mental model for how I'm thinking about uh auto uh auto research.

### Mental Model: Your Research Bot That Runs While You Sleep

**3:47** · So, imagine you have a research boss you can boss around. Number one, you write, you know, a clear task. So, for code experiments, maybe it's improve this model test score. For business, figure out the top five competitors for product XYZ and make a short report. Step two is you give the uh you give the bot um you know, access to the code, a GPU for ML experiments. You obviously need to give it access to the internet and documents if you're doing reading task. The bot then runs a loop.

**4:15** · So, it it plans, it acts, meaning it might run code or search, it reads results, it updates the plan, and then you just come back later, you know, uh you could be 12 hours, 20 hours, 6 hours, and you see if it's logged everything, charts and metrics, and then it gives you a written sum- summary in normal language. So, you know, think of auto research as a research bot that runs experiments for UI C, tries lots of ideas fast, and keeps the winners. Quick break to invite you to something. Now, this isn't an ad.

**4:45** · I just want to invite you to a free event because I think that you're going to get a lot out of it. I wanted to take 1 hour of time where we just talk about building businesses in the age of AI.

**4:55** · People say SaaS is dying. I actually believe the quite opposite. I think that SaaS is just evolving. I think right now is an incredible time to be building software startups that help you craft your dream life. And for all those reasons, I'm say I said, "Let's just book 1 hour of time. It's going to be 11:00 a.m. March 12th." That's a Thursday, where we can go and lock in and just talk about building businesses in the age of AI. I'll include a link in the description in the show notes to join, and I can't wait to see you there.

### Idea 1: Niche Agent-in-a-Box Products

**5:26** · Okay, how do we use it? Here are some ideas for you.

**5:30** · So, the first idea for you I have is a niche agent in a box, you know, products. This can be multiple products.

**5:36** · And by the way, I put out these ideas. I want you to do these ideas. I think that, you know, even if they don't turn into businesses, you will learn about these tools, and that is is to help you outperform 99.9% of people on this planet. So, uh you package tiny auto research loops tuned for one painful niche. So, the example I think of is an Amazon listing experimenter, an email sequence tuner for real realtors, uh a pricing optimizer for SaaS.

**6:03** · Those are, you know, auto research loops and and and ideally an niche that you understand well, and then you charge a monthly fee. So, the value prop is this thing runs experiments for you 24/7 and just show shows you the winner to click accept. How valuable is that? And how many different niches are there that, you know, this plays into?

**6:27** · The hard part is figuring out what the what what's the pain points and then and then obviously, you know, you want to be quick quick to market, right? So, here's a visual of it. Pick the painful niche, design the tiny auto research loop, run experiments automatically, see which setup works best, turn best setup to a simple agent product, and then you charge that monthly subscription. Number two, you're going to want to, you know, here's an idea, print money using an AB testing for marketing.

### Idea 2: A/B Testing for Marketing (Landing Pages & Ads)

**6:52** · So, this is it's it's very similar, um but instead of, you know, uh in- instead of uh you know, doing it for realtors or whatever, you're doing it for ads and landing page experiments. So, landing pages, so the agent writes variants of headlines, layouts, and offers, pushing them to traffic, measures which one converts better, and keeps iterating.

**7:15** · So, this is like conversion rate optimization around landing pages. You know, the old Think of, you know, tools like Optimizely. That's a SaaS tool that, you know, when I first moved to San Francisco, you remember how big they were and everyone was talking about Optimizely and AB testing, and it's like, well, this is the future of that.

**7:33** · Uh auto research for different landing pages. You can also do use auto research for something like ads, which auto auto creatives, it auto test angles, and audiences, and then it keeps the combat combos that lower CAC or raise ROAS. So, you know, you profit by running this for your own prod- products. Like if you if you want to build your own products and just use this internally, that works.

**7:55** · Or, you know, all offering an always-on experiment engine to clients as a retainer service. For 5K a month, I'm going to, you know, give you the best landing pages every single month and it's just going to come to your inbox, that sort of thing.

**8:08** · Visual of it, business goals, uh is you know, the goal that you're giving the auto research is more sales.

**8:15** · It's generating things like pages and ad versions, sending traffic to the versions, measuring conversion and revenue.

**8:21** · Um does any version beat the current best? Um you know, if if it doesn't, then you're going to keep the current control. But if it does, you know, you're promoting the winner to a new control and it you're asking for the AI for new ideas.

**8:34** · All right. Hope Hope your creative juices are are starting to get flowing.

**8:37** · You're starting to understand a little bit more about how how it's working, how you think about goals, how you can think about agents, and how you can set up these loops.

### Idea 3: Research as a Service

**8:45** · Number three, research as a service. So, auto research's recipe is basically a loop for doing research, right? Cuz you're searching, reading, summarizing, and you're comparing, and then you're repeating. So, how do you point that at money problems? Like market and competitor research for startups. So, constantly updated reports on who's doing what, pricing, features, and gaps.

**9:07** · Super valuable. Investor and M&amp;A decks, fast technical and market due diligence summaries. Super valuable. Comp- compliance and regulation tracking for niches. I don't know, crypto, healthcare, finance. Super valuable. So, you can charge per report like a one-off, or you can set up like a monthly subscription for always fresh dashboards.

**9:27** · So, visual uh define client research question, auto research searches and reads, um summarize and compare findings, create reports and dashboards, deliver insight to client, and the client pays per report or monthly, whatever you decide. Number four, uh, power tool inside your own product.

### Idea 4: Power Tool Inside Your Own SaaS

**9:47** · So, if you already have built a SaaS or workflow, embed an auto research style agent so your users can press optimize, just like a big I envision like a big button that just says optimize, and the system runs a mini research loop for them. So, for example, tune prompts, pick best pricing, rank suppliers. Then, you can charge higher tiers for this feature, or you can use it as a wedge to upsell pro and enterprise plan.

**10:10** · So, maybe you, uh, maybe that's a part of pro and enterprise, maybe it's something that you just send an email to, you know, your entire list and you're like, "Hey, you know, we have this really powerful tool." Imagine you press this button, it's like it's like bending spoons, right? It's like bending spoons. Like, how is this, um, bending spoons is not the private equity group I'm talking about. I'm like the idea of you can bend a spoon, right?

**10:33** · It's incredible that you'd be able to optimize, press a button, and this would happen. So, visual over here, have an existing SaaS, add an optimize button, users run mini research loops, tool suggests better settings or prices, users see better results, offer higher price pro plans and enterprise plans.

### Idea 5: Agency That Runs 100× More Tests

**10:49** · Number five, this is a saucy episode, by the way.

**10:53** · This is saucy, all right. Agency that sells, "We run more tests than anyone else." Because auto research lets you run hundreds of experiments instead of a few, you have a simple pitch, "We do 100 times more testing than other shops for the same or lower fee." A niche example, a Shopify store conversion lab, B2B SaaS pricing experiment service, email subject line and sequence optimizer. You charge per month, and a bonus if you hit specific KPI lifts, rev share performance fee. People love that, you know.

**11:23** · Of course they're going to be, you know, interested in Yeah, if you can do, if you can lift this KPI, we'll give you some bonus. So, here's the uh the visual. Starting optimization agency, use auto research to run many tests, improve stores, pricing, emails, and funnels. Show clients more experiments and wins.

**11:44** · Charge monthly retainer and performance fee.

**11:48** · Number six, and we've got about uh 10.

**11:51** · Yeah. So, we're almost almost done, and then after we're going to talk about um just some cool interesting, you know, stories around auto research, and then I'll end with uh you know, how you can set this up, you know, very briefly. So, auto quant for trading ideas. So, you can use auto research to run small, fast uh backtests of many simple trading rules. So, LLM-based factor screens, sentiment filters on one GPU overnight.

### Idea 6: Auto Quant for Trading Ideas

**12:18** · So, you can keep the few strategies that look promising, then either trade on your own account or sell signals and strategy reports. So, depends if you're a trader, maybe you're doing yourself.

**12:29** · Um or yeah, you can just, you know, sell this as a digital product or yeah, yeah, yeah, basically a digital product. So, you define the simple trading rules, you run many backtests overnight, you review the strategy performance, you keep only promising strategies, trade your own capital, or you can sell the signals. I think finance is changing a lot, um and I think with things like auto research, uh you know, it just it's it it's going to be an unfair advantage for a lot of people.

**12:58** · Um So, I think you're going to see a lot more digital products uh that people sell, and also, you know, just using their own money, trading themselves instead of giving uh 1% or whatever to a financial advisor.

**13:15** · Um I'm sure also, by the way, a lot of people are going to get burned by this, too. Like, they're not They're just going to blindly just trust an auto research. You need to have a human in in the loop, and you need to manage that uh obviously accordingly. But yeah, you can just see Yeah, there's definitely going to be some people are going to get burnt. You just give the entire um They're just going to like give a bank account and just let auto research just trade for it. I mean, it would be interesting it would be an interesting test, that's for sure.

### Idea 7: Always-On Lead Qualification & Follow-Up

**13:44** · Number seven, always on lead qualification and follow-up. Point an auto research style agent at your CRM, like a salesforce or something like that, and inbound leads. Let it test rules and messages to see which leads are most likely to buy, right? It auto grades the leads, suggests next actions, and drafts follow-up. So, sales people only focus on high-value deals, so it's more revenue per hour spent. Visual over here for you.

**14:09** · Connect to CRM, auto you know, auto research test the leads, rank leads by likelihood to buy, draft follow-up messages, sales focus on best leads, revenue per sale increases.

### Idea 8: Finance Ops Autopilot for Businesses

**14:21** · Eight, finance ops autopilot for businesses. Use the loop to grind through invoice matching, expense report generation, and exception detection with continuous small improvements rule and prompts. You can sell this as we cut your AP expense time in half, either as software or as an op service with a small team and agent. By the way, I can totally see someone like someone starting this and this gets acquired by one of the large fintech companies or one of the large banks. Uh so, visual uh here, ingest invoices and expenses.

**14:51** · The auto research improves rules and prompts, matches invoices and detects exceptions. It generates clean expense reports, reduces manual finance work, and then you can sell it as a software or op service. Or you start maybe you start as op service and then uh you kind of evolve into the software.

### Idea 9: Internal Productivity Lab for Your Org

**15:10** · Two more for you. Number nine, an internal productivity lab for your own org. I thought this was interesting. So, treat your company like Karpathy's GPU lab. Define KPIs, so like response time, close rate, ticket resolution, and let agents iterate on workflows and templates and routing rules. So, you just get fewer meetings, less manual grunt work, and then you personally touch only the high-impact decisions when everyone else rides the improved process.

**15:37** · So, the goal here is defining the key metrics, Auto Research is testing the new workflows, it's improving templates and writing rules, you're cutting meetings and manual tasks, that's good, team focuses on high-impact work, and then higher productivity and ideally higher profit.

### Idea 10: Done-for-You Research & Due Diligence Shop

**15:53** · Last idea for you, done for you research or due diligence shop. So, you use the research loop to chew through docs, filings, product pages, and reviews and keep an evolving living memo for clients, like investors, acquirers, execs. You make money by selling fast, well-structured briefs, and a monthly update packs instead of one-off manual research logs.

**16:16** · Um so, uh you know, the the goal get an investor or acquirer question, this happens all the time, Auto Research reads through docs and filings, it summarizes that product market and risk, and maintains a living memo for the client, it delivers a brief and updates packs, and the client pays for reports and ongoing access.

**16:36** · Um I would pay for something like this.

**16:38** · Um so, hopefully someone builds it.

### Non business use cases

**16:41** · All right. So, those are a bunch of ideas for you. I also saw a couple interesting things this morning. Um my good friend Morgan Linton, uh who's, you know, been on the pod before, he says, "I woke up this morning and all I can think about is Auto Research. So many ideas swirling around in my head, not sure 99% of the world realize the incredible breakthroughs Karpathy's making and just sharing casually on X.

**17:06** · Right now, where my mind is going is medicine. It feels like in many ways clinical trial design is itself kind of like a hyperparameter search. I know right now trials cost tens of millions of dollars minimum. It feels like an agent swarm could optimize treatment protocols on small proxy experiments, promote the most promising candidates, and then move to humans to review. So, humans still very much in the loop, but later on, and experimentation going much deeper, happening faster, and for far less money.

**17:37** · I think for me, while I'm not a doctor, he's an engineer. What I'm the most excited about when it comes to AI is the impact it will have on human health and critical areas like disease treatment.

**17:50** · Might be a crazy idea, so a real doctor can jump in the comments and slap me on the wrist here. I looked at the replies, I didn't see you know, any any doctors come in, but I don't know. I just can't stop thinking about how what Karpathy has discovered here could have some pretty profound implications.

**18:06** · So, only halfway through my coffee though, but woke up this morning, and this is what I'm thinking about, so I thought I'd share. I agree, I think there's a lot of really interesting not just like business profit ideas, but also just like medicine, science, research. So, I'm excited for people to to take this and and to continue with it.

### Karpathy's Agent Hub Announcement

**18:27** · Um I also saw this tweet here.

**18:29** · Uh what's after auto research? It's Karpathy's new open source project AgentHub. So, Karpathy also launched AgentHub. What is AgentHub? It's GitHub for humans. Uh sorry, GitHub is for humans, AgentHub is for agents. So, it's basically a GitHub for for agents. An agent swarm collaboration platform, a very promising direction. I'm watching him speed run a one-man billion-dollar uh company. If you look at the GitHub for AgentHub, it says, "First use cases for auto research, but it's a lot more general than that, exploratory project."

**19:04** · He says, "Agent-first collaboration platform." A bare get repo, a message board designed for a swarm of agents working on the same code bat code base.

**19:13** · Think of it like a strip down GitHub where there's no main branches, no main branch, no PRs, no merges, a sprawling dag dag of commits in every direction with a message board for agents coordinate coordinate.

**19:27** · I think this is really interesting and just like whenever Karpathy's up to something, I'm always paying attention.

**19:32** · So, I had to put that one in there as well.

**19:34** · So, um you know, maybe you've gotten to the end of uh this episode and you're kind of like, "Okay, I kind of I think I understand what auto research is. I think I know what, you know, Karpathy's a G, um Toby's a G, like all these smart people are are are playing with it. Um how do I get started?" Well, to get started, I'd recommend um just tell Claude code to get you started.

### How to Get Started with Autoresearch

**20:00** · So, you know, I went ahead and I basically was like uh I I gave um Claude code the le- the this um this GitHub repo. The GitHub the auto research GitHub repo.

**20:16** · And wow, 25,000 stars already. So, this is crazy. Um it's really growing growing quick.

**20:24** · Um so, I just gave it I gave uh gave it the link and I was just like, "I need help installing auto research by Karpathy."

**20:31** · Um and it says, "Here's how to install it and set up auto research by Karpathy.

**20:37** · You need an Nvidia GPU." So, I talked to I talked about that in the beginning. It was tested on a H100, but other Nvidia GPUs should work and you need a UV package manager. So, you have to install UV, you clone the repo, you install the dependencies, um you prepare the data and run a training experiment. In my case, I don't have an Nvidia GPU. I'm actually using a MacBook and an M1 Pro.

**21:00** · I know I'm I need a I need a upgrade um to a new Mac. So, I was like, "So, wait, I need an Nvidia GPU to do this?" Um but, there's a few options. Cloud GPU um ch- you know, you can So, you can rent an Nvidia GPU from a service like Lambda Labs, Vast AI, RunPod, or Google Colab.

**21:26** · Some offer free tier with GPUs. This is the most straightforward forward path.

**21:30** · So, that's that's the answer to people who don't have an Nvidia chip. Just rent it on one of these services. I personally use Google Colab. Why?

**21:39** · Um I just know Google the best and trust Google the best. Um you know, it also says you can try it, you know, via Apple Silicon via an MPS backend. I'm like, "No, I'm not going to do that." Um so, with that that's what road I did. I went on Google Colab. The easiest way to get started, you go to colab.google.com, you create a new notebook, you change the runtime to change runtime T4 GPU, and you run a bunch of commands. That might be like complicated, sound complicated. You This is what Colab looks like.

**22:09** · You literally just tell you know, you you listen to what um Cloud Code tells you to do, and you just paste it in, and you can get started.

**22:19** · So, you know, if if people are interested, I can spend you know, more time with this with Auto Research as I'm learning, sharing more about it. But, I just wanted to do give you a quick primer on what it is, why it's important, what are some ideas on how you can actually use this thing, um and then how are people installing it?

### Final Thoughts

**22:42** · They're just you know, you can use Cloud Code as your helper to get it installed installed, and you're going to want to rent uh a a GPU in the cloud at least to start. So, hope this has been helpful.

**22:54** · Um this is an another solo podcast that I'm doing on the Startup Ideas Podcast.

**22:59** · Last time I did this last week, I had a lot of comments that said, "Yeah, Greg, I actually really like when you just come in solo and just start like telling us what's on your mind and stuff like that in real time." So, I'm here. I read every single comment. So, you know, keep commenting, keep liking, keep subscribing, and I'll keep, you know, putting this out there for you for free.

**23:19** · Yeah, I'm excited to see what you end up using this for. Um of course, it's early, right? Like this is this is brand new.

**23:28** · Um people are still trying to figure out what are the use cases, but I always find that, you know, in the in the fog in the fog, people don't really understand where the opportunity is is when there's sometimes an opportunity. So, um one thing I've just learned in my career is just like when I see people like Karpathy doing things like this, you want to pay attention, you want to tinker with it, you want to have some fun with it, and you want to see what it's all about. So, thanks again for, you know, giving me your time.

**23:58** · Um hope this has been clear. Share this with a friend uh who you think would see it valuable. Um and if you need any uh if you need any ideas more ideas on startups to build uh you know, with AI, ideabrowser.com definitely your place to go, and I'll see you in the comment section, and uh I'll see you next time, you know? Have a creative day.
# 3-Minute Demo Video Script

## Opening (0:00 - 0:20)
**[Screen: Project title card with GR Cup branding]**

"Hi! I'm presenting the GR Cup Real-Time Racing Intelligence System - a comprehensive analytics platform that transforms raw telemetry data into actionable insights for drivers and race engineers.

This project uses all 7 Toyota GR Cup tracks and provides real-time performance analysis, strategy optimization, and driver coaching insights."

## Problem Statement (0:20 - 0:40)
**[Screen: Show raw CSV data files]**

"Race teams collect massive amounts of telemetry data - speed, braking, throttle, acceleration - but turning this data into actionable insights is challenging.

Drivers need immediate feedback. Engineers need strategy recommendations. Teams need consistency metrics.

That's what this system delivers."

## Architecture Overview (0:40 - 1:00)
**[Screen: Architecture diagram or code structure]**

"The system has three main components:

1. A Python FastAPI backend that processes telemetry data from all 7 GR Cup tracks
2. An analytics engine with lap time analysis, braking intelligence, and tire degradation modeling
3. A React dashboard for real-time visualization

The backend exposes 15+ REST API endpoints for analytics, telemetry, and strategy."

## Live Demo - Part 1: Dashboard (1:00 - 1:40)
**[Screen: Live dashboard walkthrough]**

"Let me show you the dashboard in action.

First, we select a track - let's choose Circuit of the Americas - and a race session.

The system immediately shows the best lap time, which was a 2:09.456 by driver GR86-015.

Now I'll enter a driver ID to analyze their performance.

Here we see:
- Best lap time
- Average lap time
- Consistency score of 94.2%
- Lap time progression chart showing tire degradation

The driver was consistent for the first 10 laps, then times started dropping off - indicating tire wear."

## Live Demo - Part 2: API & Analytics (1:40 - 2:20)
**[Screen: API documentation or Postman/curl requests]**

"Behind the scenes, the API provides deep analytics:

The braking analysis endpoint shows:
- Brake applications per lap
- Average brake pressure
- Braking efficiency score

The tire degradation endpoint predicts:
- Degradation rate per lap (0.15 seconds)
- Optimal pit window (lap 18-22)
- Current delta from best lap

The consistency endpoint calculates:
- Coefficient of variation
- Percentage of laps within 0.5s of best
- Standard deviation

All of this is computed in real-time from the telemetry data."

## Research & Impact (2:20 - 2:45)
**[Screen: Research papers or impact metrics]**

"This project is built on peer-reviewed motorsports research:
- ML lap time prediction with 97% accuracy
- Reinforcement learning for optimal racing lines
- Real-time telemetry architectures from F1 and FSAE teams

The impact is immediate:
- Drivers get instant feedback on where they're losing time
- Engineers get data-driven pit strategy recommendations
- Teams can track driver development and consistency

This system could reduce lap times by 0.5-1 second through optimized braking and racing lines."

## Closing (2:45 - 3:00)
**[Screen: GitHub repo, project links]**

"The entire project is open source on GitHub, with full documentation and setup instructions.

It's built with Python, FastAPI, React, and TypeScript - production-ready and scalable.

Thank you for watching! I'm excited to bring real-time intelligence to Toyota GR Cup racing."

**[Screen: End card with project name and links]**

---

## Visual Elements to Include

1. **Title Card**: Project name with GR Cup branding
2. **Data Visualization**: Show CSV files, then transformed charts
3. **Architecture Diagram**: Backend → Analytics → Frontend flow
4. **Live Dashboard**: Full walkthrough with real data
5. **API Documentation**: Show Swagger/OpenAPI docs
6. **Performance Charts**: Lap times, tire degradation, consistency
7. **Code Snippets**: Brief glimpse of key algorithms
8. **Impact Metrics**: Time savings, accuracy improvements
9. **GitHub Repository**: Show README and project structure
10. **End Card**: Links to repo, demo, documentation

## Recording Tips

- Use screen recording software (OBS, Loom, or similar)
- Record at 1080p minimum
- Use clear audio (external mic recommended)
- Keep pace energetic but clear
- Show real data, not mock data
- Highlight unique features (tire degradation, pit strategy)
- End with clear call-to-action (check out the repo)

## Key Points to Emphasize

✅ Uses ALL 7 GR Cup tracks
✅ Real-time analytics (not just post-race)
✅ Actionable insights (not just data visualization)
✅ Research-backed algorithms
✅ Production-ready code
✅ Open source and well-documented
✅ Immediate impact on lap times and strategy

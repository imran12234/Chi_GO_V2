# ChiGo – AI-Powered Trip Planning Web App

**ChiGo** is a full-stack AI-powered trip planning application that generates personalized, multi-day Chicago itineraries using structured user preferences, constrained LLM outputs, and real-world location data.

🔗 **Live Demo:** https://chi-go-v2.onrender.com

---

## Overview

ChiGo helps users plan trips by combining structured survey inputs with controlled AI generation and external mapping services. Instead of free-form text generation, the system enforces deterministic structure, validates outputs, and enriches recommendations with real-world data.

The project emphasizes **backend system design, responsible LLM integration, and production deployment**.

---

## Key Features

- Personalized multi-day itinerary generation using OpenAI GPT-4o-mini  
- Structured survey-based preference collection (cuisine, activity level, budget, neighborhoods)  
- Schema-guided AI prompting with enforced JSON output  
- Activity enrichment with real coordinates, addresses, photos, and ratings via Google Places API  
- Interactive activity-swapping system with AI-generated alternatives  
- Transit time calculation between itinerary stops using Google Routes API with Haversine fallback  
- Persistent storage of trips and activities with session-aware updates  

---

## System Architecture

### Backend
- Django-based MVC architecture  
- ORM-backed relational data models  
- Form-driven survey validation and normalization  
- Business logic layer for itinerary orchestration and updates  

### AI Layer
- OpenAI GPT-4o-mini for itinerary generation  
- Prompt pipeline enforcing:
  - Exact number of days  
  - Day-by-day activity structure  
  - Distance and neighborhood constraints  
- Separation of AI logic from application logic to prevent hallucinations  

### External Services
- **Google Places API** for validating and enriching activities  
- **Google Routes API** for walk/drive transit time estimation  
- Haversine distance fallback for geospatial robustness  

### Data Layer
- PostgreSQL for persistent storage  
- Normalized models for itineraries, activities, and preferences  

---

## Example Workflow

1. User completes a structured trip survey (dates, cuisine, activity level, budget, neighborhood)  
2. Backend validates and normalizes survey inputs  
3. AI prompt pipeline generates a constrained, structured itinerary  
4. Activities are enriched with real-world data and coordinates  
5. Transit times between consecutive stops are calculated  
6. Itinerary is stored and rendered in the user dashboard  
7. Users can swap individual activities with AI-generated alternatives in real time  

---

## Tech Stack

- **Language:** Python  
- **Framework:** Django  
- **Database:** PostgreSQL  
- **AI:** OpenAI GPT-4o-mini  
- **APIs:** Google Places API, Google Routes API  
- **Deployment:** Docker, Render, Gunicorn  
- **Other:** Django ORM, WhiteNoise, Session Management  

---

## Deployment

ChiGo is containerized with Docker and deployed to Render using:

- Gunicorn application server  
- Managed PostgreSQL database  
- WhiteNoise for static file serving  

---

---
title-prefix: Home
template:
  home: true
collections:
  - name: games
    key: playing
    filter-by:
      key: state
      value: active
  - name: games
    key: completed
    filter-by:
      key: state
      value: completed
    first: 3
  - name: blog
    first: 3
  - name: thoughts
    first: 3
    content: true
  - name: leetcode
    first: 4
header-includes: |-
  <style>
    br {
      display: none;
    }

    img, video {
      aspect-ratio: 16 / 9;
      object-fit: contain;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 2.5em;
    }

    .section-header h3 {
      margin: 0;
    }

    .section-header a {
      display: flex;
      align-items: center;
      text-decoration: none;
      color: var(--c4);
    }

    .section-header a:hover {
      text-decoration: underline;
    }
    .thoughts ul {
      padding: 0;
    }

    .thoughts li {
      list-style-type: none;
      padding: 0;
    }

    .thoughts li {
      background-color: var(--c1);
      border: 1px solid var(--c5);
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 16px;
      font-family: var(--sans);
      color: var(--c2);
    }

    .thoughts li div:first-of-type {
      margin-bottom: 10px;
    }

    .thoughts li a {
      color: var(--c3);
    }

    .thoughts li a:hover {
      color: var(--c4);
    }

    .thoughts li div {
      margin: 0;
      line-height: 1.6;
    }

    .blogs {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      padding: 1rem;
      padding-left: 0;
    }

    .blog {
      background-color: var(--c5);
      border: 1px solid var(--c6);
      padding: 1rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
    }

    .blog-title {
      font-weight: bold;
      margin-bottom: 0.5rem;
    }

    .blog-date {
      font-size: 0.9rem;
      color: var(--c4);
      margin-bottom: 0.5rem;
    }

    .blog a {
      text-decoration: none;
      color: inherit;
    }

    .blog a:hover {
      text-decoration: underline;
    }

    .games {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      padding: 1rem 0;
    }

    .game {
      position: relative;
      background-color: var(--c5);
      border: 1px solid var(--c6);
      overflow: hidden;
      width: 100%;
      height: 240px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      display: flex;
      flex-direction: column;
    }

    @media (width < 600px) {
      .games {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    .game img {
      width: 100%;
      height: 90px;
      display: block;
      object-fit: cover;
    }

    .game a {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
    }

    .game-info {
      padding: 0.5rem;
      text-align: left;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }

    .game-info span {
      color: var(--c2);
    }

    .game-info img {
      margin-right: 0.5rem;
      width: 18px;
      height: 18px;
      filter: invert(1);
      margin: 0;
    }

    .game-title {
      font-weight: bold;
      display: block;
      flex: 1;
    }

    .footer {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .game-date, .game-state {
      font-size: 0.9rem;
      color: var(--c4);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .game-playing {
      border-color: var(--status-active);
    }

    .game-completed {
      border-color: var(--status-completed);
    }
  </style>
---

### Welcome to My Space on the Internet

Hi, I'm **Mahmoud Ashraf** 👋.
Based in **Alexandria, Egypt**, I'm a **Software Engineer** who makes websites.
I write about **Tech, Linux, Privacy, and Front-end Development**.
Instead of using social media, I share my **posts and photos** here.!!

[Learn More About Me](/about)

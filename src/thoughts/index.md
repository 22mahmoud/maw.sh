---
title-prefix: thoughts
thoughts-template: true
pagination:
  collection: thoughts
  page-size: 10
  page-path: page
  content: true
header-includes: |-
  <style>
    br {
      display: none;
    }

    .thoughts ul {
      padding: 0;
    }

    img, video {
      aspect-ratio: 16 / 9;
      object-fit: contain;
    }

    .thoughts li {
      list-style-type: none;
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

    .thoughts .navigation {
      text-align: right; /* Aligns navigation links to the right */
      margin-top: 10px; /* Optional: Adjust margin as needed */
    }

    .thoughts .navigation a {
      margin-left: 10px; /* Adds spacing between Prev and Next links */
    }
  </style>
---

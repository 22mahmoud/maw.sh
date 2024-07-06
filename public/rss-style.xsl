<?xml version="1.0" encoding="utf-8"?>
<!--

# Pretty Atom Feed

Based on "Pretty RSS Feed": https://github.com/genmon/aboutfeeds/issues/26

-->
<xsl:stylesheet
    version="3.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:atom="http://www.w3.org/2005/Atom">
	<xsl:output method="html" version="4.0" encoding="UTF-8" indent="yes"/>
	<xsl:template match="/">
		<html
			xmlns="http://www.w3.org/1999/xhtml" lang="en">
			<head>
				<meta charset="utf-8"/>
				<meta name="viewport" content="width=device-width, initial-scale=1"/>
				<title>
					<xsl:value-of select="atom:feed/atom:title"/>
				</title>
        <style type="text/css">

          :root {
            /* fonts */
            --sans: 1em/1.6 system-ui, -apple-system, BlinkMacSystemFont, Segoe UI,
              Roboto, Oxygen, Ubuntu, Cantarell, Droid Sans, Helvetica Neue, Fira Sans,
              sans-serif;
            --mono: SFMono-Regular, Consolas, "Liberation Mono", Menlo, Courier,
              "Courier New", monospace;

            /* colors */
            --c1: #080808;
            --c2: #f1f2f2;
            --c3: #5db3fd;
            --c4: #ebdbb2;
            --c5: #1d2021;
            --c6: #b0b0b0;

            --status-active: #28a745;
            --status-wanted: #ffc107;
            --status-completed: #17a2b8;
          }

          *,
          *::before,
          *::after {
            box-sizing: border-box;
          }

          html {
            -moz-text-size-adjust: none;
            -webkit-text-size-adjust: none;
            text-size-adjust: none;
          }

          body,
          h1,
          h2,
          h3,
          h4,
          p,
          figure,
          blockquote,
          dl,
          dd {
            margin-block-end: 0;
          }

          ul[role="list"],
          ol[role="list"] {
            list-style: none;
          }

          body {
            min-height: 100vh;
            line-height: 1.5;
          }

          h1,
          h2,
          h3,
          h4,
          button,
          input,
          label {
            line-height: 1.1;
          }

          h1,
          h2,
          h3,
          h4 {
            text-wrap: balance;
          }

          a:not([class]) {
            text-decoration-skip-ink: auto;
          }

          img,
          picture {
            max-width: 100%;
          }

          input,
          button,
          textarea,
          select {
            font-family: inherit;
            font-size: inherit;
          }

          textarea:not([rows]) {
            min-height: 10em;
          }

          :target {
            scroll-margin-block: 5ex;
          }

          address,
          area,
          article,
          aside,
          audio,
          blockquote,
          datalist,
          details,
          dl,
          fieldset,
          figure,
          form,
          input,
          iframe,
          img,
          meter,
          nav,
          ol,
          optgroup,
          option,
          output,
          p,
          pre,
          progress,
          ruby,
          section,
          table,
          textarea,
          ul,
          video {
            /* Margins for most elements */
            margin-bottom: 1rem;
          }

          hr {
            border: 0;
            border-bottom: 1px solid var(--c5);
            margin: 1rem auto;
          }

          body {
            margin: 0 auto;
            padding: 1em;
            font: var(--sans);
            font-weight: 400;
            line-height: 1.5;
            background: var(--c1);
            color: var(--c2);
            max-width: 768px;
            display: flex;
            flex-direction: column;
            height: 100vh;
          }

          main {
            flex: 1;
          }

          figure {
            margin: 0;
            margin-bottom: 1rem;
            padding: 0.625em;
            border: 1px solid var(--c1);
            text-align: center;
            background-color: var(--c5);
            font-family: var(--sans);
          }

          figure img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
          }

          figcaption {
            margin-top: 0.625em;
            font-size: 0.9em;
            color: var(--c4);
          }

          img {
            height: auto;
            max-width: 100%;
          }

          video {
            width: 100%;
            aspect-ratio: 16 / 9;
          }

          video {
            width: 100%;
            height: 100%;
          }

          a {
            color: var(--c3);
            text-decoration: none;
          }

          a:hover {
            text-decoration: underline;
          }

          pre {
            background: var(--c5);
            color: var(--c4);
            padding: 1em;
            overflow: auto;
          }

          code {
            font: 1em/1.6 var(--mono);
            color: var(--c4);
          }

          .highlighted-word {
            background-color: #202127;
            border: 1px solid #3c3f44;
            padding: 1px 3px;
            margin: -1px -3px;
            border-radius: 4px;
          }

          blockquote {
            border-left: 5px solid var(--c5);
            color: var(--c4);
            padding: 1em 1.5em;
            margin: 0;
          }

          summary {
            cursor: pointer;
            font-weight: bold;
          }

          details[open] {
            padding-bottom: 0.75rem;
          }

          details {
            background: var(--c5);
            padding: 1rem;
          }

          details pre {
            background: var(--c1);
            white-space: pre-line;
          }

          details[open] summary {
            margin-bottom: 6px;
          }

          details[open] > *:last-child {
            margin-bottom: 0;
          }

          /* Headlines */
          h1,
          h2,
          h3,
          h4,
          h5,
          h6 {
            line-height: 1;
            padding-top: 0.875rem;
          }

          h1,
          h2,
          h3 {
            padding-bottom: 2px;
            margin-bottom: 8px;
          }

          h4,
          h5,
          h6 {
            margin-bottom: 0.3rem;
          }

          h1 {
            font-size: 2.25rem;
          }

          h2 {
            font-size: 1.85rem;
          }

          h3 {
            font-size: 1.55rem;
          }

          h4 {
            font-size: 1.25rem;
          }

          h5 {
            font-size: 1rem;
          }

          h6 {
            font-size: 0.875rem;
          }

          ol,
          ul {
            /* Replace the browser default padding */
            padding-left: 2rem;
          }

          li {
            margin-top: 0.4rem;
          }

          ul ul,
          ol ul,
          ul ol,
          ol ol {
            margin-bottom: 0;
          }

          footer {
            padding-top: 1.5em;
            padding-bottom: 1em;
          }

          noscript {
            background: #f9c642;
            color: black;
            padding: 10px;
            border-radius: 8px;
            display: block;
          }

          .site-title a {
            color: var(--c2);
            font-weight: bold;
          }

          .nav {
            margin-bottom: 1em;
          }

          .nav ul {
            display: flex;
            padding: 0;
            flex-wrap: wrap;
          }

          .nav ul li {
            list-style-type: none;
            margin-bottom: 0.3em;
          }

          .nav ul li:not(:last-child) {
            margin-right: 0.8em;
          }

          .theme-toggle a {
            color: var(--c2);
            background-color: var(--c5);
            padding: 0.25em 0.5em;
            border-radius: 99999999px;
          }

          .theme-toggle > a:hover {
            text-decoration: none;
          }

          /* Article Styling */
          article.h-entry {
            padding: 1em;
            border: 1px solid var(--c5);
            margin-bottom: 1.5em;
            border-radius: 8px;
          }

          /* Header Styling */
          article.h-entry header {
            margin-bottom: 1em;
          }

          article.h-entry time.dt-published {
            display: block;
            color: var(--c3);
            font-weight: bold;
            font-size: 0.9em;
          }

          /* Content Styling */
          article.h-entry section.e-content {
            font-size: 1em;
            line-height: 1.6;
            color: var(--c2);
          }

          /* Footer Styling */
          article.h-entry footer {
            margin-top: 1em;
            font-size: 0.8em;
            color: var(--c6);
          }
        
          </style>
			</head>
			<body>
				<nav class="container">
					<p class="about">
						<strong>This is a web feed,</strong> also known as an RSS or Atom feed.
						<br />
						<strong>Subscribe</strong> by copying the URL from the address bar into your newsreader.
          
					</p>
					<p class="gray">
            Visit 
						<a href="https://aboutfeeds.com">About Feeds</a> to get started with newsreaders and subscribing. It’s free.
          
					</p>
				</nav>
				<div class="container">
					<h2>Recent Items</h2>
					<xsl:apply-templates select="atom:feed/atom:entry" />
				</div>
			</body>
		</html>
	</xsl:template>
	<xsl:template match="atom:feed/atom:entry">
		<div class="item">
			<h3>
				<a>
					<xsl:attribute name="href">
						<xsl:value-of select="atom:link/@href"/>
					</xsl:attribute>
					<xsl:value-of select="atom:title"/>
				</a>
			</h3>
			<small class="gray">
        Published: 
				<xsl:value-of select="atom:updated" />
			</small>
			<xsl:choose>
				<xsl:when test="/atom:feed/atom:id='rss-thoughts.xml'">
					<div style="border-bottom: 1px solid #eaecef;">
						<xsl:apply-templates select="atom:content"/>
					</div>
				</xsl:when>
				<xsl:otherwise></xsl:otherwise>
			</xsl:choose>
		</div>
	</xsl:template>
	<xsl:template match="atom:content">
		<div>
			<xsl:value-of select="." disable-output-escaping="yes"/>
		</div>
	</xsl:template>
</xsl:stylesheet>

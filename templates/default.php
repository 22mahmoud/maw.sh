<?php ?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link
      rel="alternate"
      type="application/rss+xml"
      href="$base_url$/rss.xml"
      title="Mahmoud Ashraf's blog feed"
    />
    <link
      rel="alternate"
      type="application/rss+xml"
      href="$base_url$/rss-thoughts.xml"
      title="Mahmoud Ashraf's thoughts feed"
    />

    <link
      rel="canonical"
      href="$base_url$$if(canonical)$$canonical$$else$$path$$endif$"
    />

    <link rel="shortcut icon" href="/favicon.ico" />
    <link rel="icon" type="image/png" sizes="16x16" href="/images/images/favicon-16x16.png" />
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png" />
    <link href="/images/favicon-180x180.png" rel="apple-touch-icon" sizes="180x180" />
    <link rel="manifest" href="/manifest.json" />
    <meta name="theme-color" content="#080808" />
    <link type="text/plain" rel="author" href="$base_url$/humans.txt" />

    <link rel="me" href="https://x.com/maw_sh" />
    <link rel="me" href="https://reddit.com/user/22mahmoud_" />
    <link rel="pgpkey authn" href="$base_url$/gpg-key.gpg" />
    <link
      rel="me"
      href="https://pixelfed.social/i/web/profile/201636586306277376"
    />
    <link rel="authorization_endpoint" href="https://indieauth.com/auth" />
    <link rel="token_endpoint" href="https://tokens.indieauth.com/token" />
    <link rel="webmention" href="https://webmention.io/maw.sh/webmention" />
    <link rel="pingback" href="https://webmention.io/sia.codes/xmlrpc" />
    <meta name="fediverse:creator" content="@22mahmoud@fosstodon.org" />
    <meta property="og:locale" content="en_US">
    <meta
      property="og:title"
      content="$if(title-prefix)$$title-prefix/nowrap$ – $endif$$pagetitle$"
    />
    <meta property="og:description" content="$description-meta$" />
    <meta property="og:type" content="$if(post)$article$else$website$endif$" />
    <meta property="og:url" content="$base_url$$path$" />
    <meta
      property="og:image"
      content="$if(og-image)$$base_url$$og-image.photo.original$$elseif(featured-image.photo)$$base_url$$featured-image.photo.original$$else$$base_url$/images/avatar.webp$endif$"
    />
    <meta property="og:site_name" content="Mahmoud Ashraf" />
    <meta property="og:locale" content="$locale$" />
    <meta
      name="twitter:card"
      content="$if(post)$summary_large_image$else$summary$endif$"
    />

    $if(post)$

    <script type="application/ld+json">
    {
      "@context": "http://schema.org",
      "@type": "BlogPosting",
      "headline": "$title-prefix/nowrap$",
      "image": "$if(og-image)$$base_url$$og-image.photo.original$$elseif(featured-image.photo)$$base_url$$featured-image.photo.original$$else$$base_url$/images/avatar.webp$endif$",
      "datePublished": "$date$",
      "dateModified": "$if(last_modified)$$last_modified$$else$$date$$endif$",
      "author": {
        "@type": "Person",
        "name": "$author$",
        "url": "$base_url$"
      },
      "publisher": {
        "@type": "Organization",
        "name": "$author$",
        "logo": {
          "@type": "ImageObject",
          "url": "$base_url$/images/avatar.webp"
        }
      },
      "description": "$description-meta$",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "$base_url$/$path$"
      }
    }
    </script>

    $else$

    <script type="application/ld+json">
    {
      "@context": "http://schema.org",
      "@type": "WebSite",
      "name": "$author$",
      "description": "$description-meta$",
      "url": "$base_url$",
      "image": "$base_url$/images/avatar.webp",
      "author": {
        "@type": "Person",
        "name": "$author$"
      },
      "sameAs": [
        "https://github.com/22mahmoud",
        "https://x.com/maw_sh",
        "https://reddit.com/user/22mahmoud_",
        "https://pixelfed.social/i/web/profile/201636586306277376"
      ]
    }
    </script>

    $endif$


    $for(author-meta)$
    <meta name="author" content="$author-meta$" />
    $endfor$

    $if(date-meta)$
    <meta name="dcterms.date" content="$date-meta$" />
    $endif$

    $if(keywords)$
    <meta name="keywords" content="$for(keywords)$$keywords$$sep$, $endfor$" />
    $endif$

    $if(description-meta)$
    <meta name="description" content="$description-meta$" />
    $endif$

    <title>$if(title-prefix)$$title-prefix$ – $endif$$pagetitle$</title>

    $for(css)$
    <link rel="stylesheet" href="$css$" />
    $endfor$ 

    $if(game)$ 
    <link rel="stylesheet" href="/css/game.css" />
    $endif$

    $if(post)$ 
    <link rel="stylesheet" href="/css/webmentions.css" />
    $endif$

    $if(thought)$ 
    <link rel="stylesheet" href="/css/webmentions.css" />
    $endif$

    $for(header-includes)$ $header-includes$ $endfor$
  </head>

  <body>
    <header>
      <p class="site-title">
        <a href="/"> maw.sh </a>
        <span>&gt; Mahmoud Ashraf Website </span>
      </p>
      <nav class="nav">
        <ul>
          <li><a href="/about/"> /About </a></li>
          <li><a href="/blog/"> /Blog </a></li>
          <li><a href="/thoughts/"> /Thoughts </a></li>
          <!-- <li><a href="/photos/"> /Photos </a></li> -->
          <li><a href="/uses/"> /Uses </a></li>
          <li><a href="/contact/"> /Contact </a></li>
          <li><a href="/tracker/"> /tracker </a></li>
          <li><a href="/cv.txt"> /cv </a></li>
          <li><a href="/rss.xml"> /rss </a></li>
          <li class="theme-toggle"><a href="/light/"> ☀ light mode </a></li>
        </ul>
      </nav>
    </header>

    <main>
      $for(include-before)$ $include-before$ $endfor$

      $if(submission)$
      <div style="border: 3px solid var(--c5); padding: 0.8rem">
        <h2 style="margin: 0 0 10px">
          $id$. $title-prefix$
          <a href="$submission$" target="_blank" style="font-size: 1rem">🔗</a>
        </h2>
        <p><strong>Date:</strong> $date$</p>
        <p><strong>Tags:</strong> $for(keywords)$<a href="/tags/$keywords$/">$keywords$</a>$sep$, $endfor$</p>
        <details>
          <summary>Description</summary>
          $description$
        </details>
      </div>
      $endif$

      $if(home)$ ${home.html()}
      $elseif(thoughts)$ ${thoughts.html()}
      $elseif(games)$ ${games.html()}
      $elseif(tags-page)$ ${tags.html()}
      $elseif(tag-page)$ ${tag.html()}
      $elseif(blog)$ ${blog.html()}
      $elseif(post)$ ${post.html()}
      $elseif(thought)$ ${thought.html()}
      $elseif(game)$ ${game.html()}
      $else$ $body$ ${author.html()} $endif$

      $for(include-after)$ $include-after$ $endfor$
    </main>

    <footer>
      <div class="wb-wrapper">
        <a
          aria-label="Support PALESTINE badge"
          href="https://techforpalestine.org/learn-more"
        >
          <div class="wb" style="outline-color: #06512a">
            <div>🇵🇸</div>
            <div style="background-color: #06512a">PALESTINE</div>
          </div>
        </a>

        <a aria-label="maw.sh rss feed" href="/rss.xml">
          <div class="wb" style="outline-color: #9c3607">
            <div><img loading="lazy" alt="rss logo" src="/images/rss.svg" /></div>
            <div style="background-color: #9c3607; color: #fff">
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RSS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </div>
          </div>
        </a>

        <a aria-label="pandoc website" href="https://pandoc.org/">
          <div class="wb" style="outline-color: #000">
            <div>
              <img
                loading="lazy"
                alt="pandoc logo"
                src="/images/pandoc.svg"
                style="width: 18px; height: 18px"
              />
            </div>
            <div style="background-color: #000; color: #fff">
              &nbsp;&nbsp;&nbsp;Pandoc&nbsp;&nbsp;&nbsp;
            </div>
          </div>
        </a>

        <a
          aria-label="vultr vps referral link"
          href="https://www.vultr.com/?ref=9553782-8H"
        >
          <div class="wb" style="outline-color: #0256b1">
            <div style="background-color: #c9f4ff; color: #000">VPS</div>
            <div style="background-color: #0256b1">VULTR</div>
          </div>
        </a>

        <a
          aria-label="My Mastodon account"
          rel="me"
          href="https://fosstodon.org/@22mahmoud"
        >
          <div class="wb" style="outline-color: #5437c7">
            <div>
              <img loading="lazy" alt="Mastodon logo" src="/images/mastodon.svg" />
            </div>
            <div style="background-color: #5437c7">Mastodon</div>
          </div>
        </a>

        <a
          aria-label="My Github account"
          rel="me"
          href="https://github.com/22mahmoud"
        >
          <div class="wb" style="outline-color: #000">
            <div>
              <img
                loading="lazy"
                alt="github logo"
                src="/images/gh.svg"
                style="width: 22px; height: 22px"
              />
            </div>
            <div style="background-color: #000; color: #fff">
              &nbsp;&nbsp;&nbsp;Github&nbsp;&nbsp;&nbsp;
            </div>
          </div>
        </a>

        <a
          aria-label="My Youtube account"
          rel="me"
          href="https://www.youtube.com/@22mahmoud"
        >
          <div class="wb" style="outline-color: #cd1508">
            <div>
              <img
                loading="lazy"
                alt="youtube logo"
                src="/images/yt.svg"
                style="width: 22px; height: 22px"
              />
            </div>
            <div style="background-color: #cd1508; color: #fff">
              &nbsp;&nbsp;Youtube&nbsp;&nbsp;
            </div>
          </div>
        </a>
      </div>

      <div
        style="
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 10px;
          margin-top: 15px;
        "
      >
        <div
          style="
            width: fit-content;
            display: flex;
            justify-content: center;
            align-items: center;
          "
        >
          <a
            style="text-align: center; width: 32px; display: block"
            href="https://xn--sr8hvo.ws/previous"
          >
            ←
          </a>
          <a href="https://xn--sr8hvo.ws"> IndieWeb Webring 🕸💍 </a>
          <a
            style="text-align: center; width: 32px; display: block"
            href="https://xn--sr8hvo.ws/next"
          >
            →
          </a>
        </div>
      </div>

      <div style="margin-top: 15px; text-align: center">
        © <a href="https://maw.sh"> Mahmoud Ashraf </a>
      </div>
    </footer>

    <script
      integrity="sha384-QfJMxHNngbaF6IXH2kBwubsLYh7GVSFmJOX1O1YKJBq+zv1VVypB9BysTzyG1D1U"
      data-goatcounter="https://stats.maw.sh/count"
      async
      src="$base_url$/js/count.js"
      crossorigin="anonymous"
    ></script>
  </body>
</html>
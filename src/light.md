## Light Mode

This site is only available in dark color scheme. 

If you prefer the light mode or any color scheme,
You can inject your custom css by changing the `css variables`

It depends on you browser if you are using firefox, or chromium based browser,
install [Stylus](https://github.com/openstyles/stylus/).

### Why Not?

- because I love the dark theme.
- and I don't want load javascript in my site.
- I don't want use css solution `prefers-color=scheme` without toggle
functionality which depends on javascript.

### Example:

```css
/* custom-style.css */

/* light mode */
:root {
  --c1: #f1f2f2; /* background */
  --c2: #080808; /* forground */
  --c3: #185488; /* link      */
  --c4: #3c3836; /* code tag forground */
  --c5: #fbf1c7; /* code tag background */ 
}

hr {
  border-color: var(--c4);
}

blockquote {
  border-color: var(--c4);
}

```

## Light Mode

This site is only available in dark color scheme. 

If you prefer the light mode or any color scheme,
You can inject you custom css by changing the `css variables`

It depends on you browser if you are using firefox, or chromium based browser,
install [Stylus](https://github.com/openstyles/stylus/).

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

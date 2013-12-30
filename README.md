Simple--Blog--Django-App
========================

My personal website written in Django.

- Ajaxified/History API: page contents are loaded via ajax and pushed onto the browser history stack. I decided to write my own rather than use the heavier ajaxify plugin. (I only load page content, new scripts, etc, rather than the whole page)
- animate.css: fnacy css animation to show off when a new page loads, or to point how people can contact me
- "funky header image" - darkens as you scroll down
- responsive: should look reasonable on mobile, tablet and desktop.

Each page is an instance in the database. It can belong to different categories, such as "blogpost", "static", etc.


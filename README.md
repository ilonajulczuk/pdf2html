# Goal

My original problem was that on desktop I read pdfs, on mobile I read web
or kindle. I would like to have a shared reading experience.

Sometimes I read white papers or long books, how lovely it would be if I could
read them on my phone as well (not as pdf, unreadable bastards!).

So the goal of this project is to build a private place on the web,
 where you can place your pdf files and convert them
to easily digestible html files.

Those html files are nice because, layout can adapt to any device size, yay!

No more horrible reading experience with pdf on mobile.

Morevoer, you can partition your pdf file into digestible chunks, so that you
could read it on mobile, with for example pocket.

Maybe in the future, I will create a mobile app, who knows?

# Design

I don't need super duper frontend. Just simple html would be fine.

I need:
- users + session
- storage for documents
- storage for documents in html
- documents having its partitions, e.g partitioned into 10 parts
- documents or partitions having their metadata
- something in background doing document conversions

Maybe i could have a dashboard for a user with his documents.
I want to minimize dependencies as much as possible.

# Tech

I know python and I know django. I can use celery for background processing,
even though it's a little bit of overkill.

This should be straightforward enough.



---
sudo apt-get install libjpeg-dev



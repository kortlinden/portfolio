Final Project Udacity Data Visualization
References:
Udacity Data Visualization animation example based on "World Cup" data.
And, the d3 map example found at the following link.
http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922

In this project, I sought to visualize all of the places I have lived in my
29 years on earth.  I thought it would be nice to see the data presented
chronologically, graphically, as well as allow for interaction so that
visitors can click through to compare my moves.

Feedback:
I drew my first iteration on paper (see attached image, paperdraft.jpg), but
when I compiled my data, I realized that I had not included the UK, where I had
lived for 1 year.  You will see the addition in red.

Juan's comments:
I then created the first working html file, but after showing it to my
husband, he suggested that I add a dynamic title which would display the year
as each dot moved. Additionally, he suggested I zoom as much as possible onto
the US without cutting out the UK.  I made the changes suggested.

At this point, I had what you see as iteration 1 (see index.html) - also this uses
data file kortlife1.tsv which is slightly different than kortlife2.tsv which
corresponds to final_index.html.

I then sent this to my friends Cely and Rodrigo.

Rodrigo's comments:
"I think the orange is kind of an ugly choice, and I think that you should
show the rest of the countries as a reference since its hard to tell the UK
is the UK without them. I would color the other countries that you have not lived
a different color so that the eye will go to the locations you have lived."

Cely's comments:
"I like how you can see all of the the movement, but it seems to me that the
map may be improved by making the circle size change relative to how long you
might actually have lived in a given place.  Also, it would be nice to have the
state lines for reference."

Design:
I implemented the zoom and pan that Juan suggested and added the changing
title to reflect the year of each move. I changed the orange circles out for
yellow which stands out but is still pleasing with the light blue and green.
I also made the rest of the countries display in a BLUE color instead of being
invisible. This really helped identify the UK as the UK. Additionally,
I took my reviewer's suggestion to highlight the country of focus in the green
and the rest in blue which helps.  I made the circle size correspond to the relative
amount of time I have lived in a place and added a note as a static title.
To make this change, I had to add the data to my
tsv file. I tried many times to locate a geo json with world
countries and the US state lines but I was unsuccessful and so did not implement that suggested change.    

Insights learned from this visualization:
Primarily, you see many moves, in fact, 17 buttons display showing 17 moves.
That's more than once every 2 years! Additionally, the map shows that almost
all of that time was spent in the USA.  Furthermore, even though I've moved
so often, the map shows that I spent my time in 4 general regions in the USA.
1. Southern California
2. The Pacific Northwest
3. East Coast
4. Midwest

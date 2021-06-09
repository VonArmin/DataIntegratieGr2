# groep 2: Jung Ho, Rutger, Armin
Dit is de githubpagina voor dataintergatie van groepje 2

Het doel van dit project was het maken van een workflow.
De workflow moet VCF data inladen, deze annoteren, mappen naar het OMOP model en deze in een database zetten.

# UseGalaxy
Om de data in te laden en te annoteren hebben we gebruik gemaakt van UseGalaxy;
[Link naar galaxy workflow](https://usegalaxy.org/u/armin1994/w/dataintegratie)

Met galaxy hebben we geprobeerd de data in te laden, te filteren op chromosoom 21 en deze te annoteren.

Het filteren is gedaan door bcftools filter, waar we een region filter toe kunnen voegen. Dit filter is ingesteld op chr21.
De data is vervolgens gecontroleerd, dit was in orde.

Het annoteren is in eerste instantie gedaan door de SnpEff tool in galaxy.
De data is vervolgens gecontroleerd, er was niets geannoteerd.

We hebben een hoop met de parameters van de tool gespeeld maar geen een parameter leek iets aan de output te veranderen.

We hebben uiteindelijk de data via de commandline met SnpEff geannoteerd, dat werkte wel.

Omdat de tools niet correct leken te werken zijn we zonder UseGalaxy veder gegaan met de intantie het via een bash script te doen.

# Usagi

Om de data te mappen naar het OMOP Datamodel wilden we Usagi gebruiken. 
We hebben daarvoor vocabulary files van Athena gedownload en deze in usagi geladen.
Dit verliep niet echt soepel, usagi gaf telkens een error terug waarin stond dat er niet genoeg ruimte was.





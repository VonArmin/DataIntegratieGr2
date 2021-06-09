# Groep 2: Jung Ho, Rutger, Armin
Dit is de githubpagina voor dataintegratie van groepje 2

Het doel van dit project was het maken van een workflow.
De workflow moet VCF data inladen, deze annoteren, mappen naar het OMOP model en deze in een database zetten.

# UseGalaxy
Om de data in te laden en te annoteren hebben we gebruik gemaakt van UseGalaxy;
[Link naar galaxy workflow](https://usegalaxy.org/u/armin1994/w/dataintegratie)
(om de workflow te bekijken moet je even op import workflow rechtsbovenin klikken)

Met galaxy hebben we geprobeerd de data in te laden, te filteren op chromosoom 21 en deze te annoteren.

Het filteren is gedaan door bcftools filter, waar we een region filter toe kunnen voegen. Dit filter is ingesteld op chr21.
De data is vervolgens gecontroleerd, dit was in orde.

Het annoteren is in eerste instantie gedaan door de SnpEff tool in galaxy.
De data is vervolgens gecontroleerd, er was niets geannoteerd.

We hebben een hoop met de parameters van de tool gespeeld maar geen een parameter leek iets aan de output te veranderen.
Omdat de tools niet correct leken te werken zijn we zonder UseGalaxy veder gegaan met de intentie het via een bash script te doen.

We hebben alleen de gefilterde data uit UseGalaxy gebruikt om mee verder te werken.

# Annotatie

We hebben de data via de commandline met SnpEff geannoteerd, dat werkte wel:

java -jar -Xmx8g -jar snpEff.jar -v GRCh37.75  patient_file12.csv > patient_file12.ann.csv

vervolgens zijn dmv SnpSift de missense varianten opgeslagen:

java -jar SnpSift.jar filter "ANN[0].EFFECT has 'missense_variant'" examples/test.chr22.ann.vcf > test.chr22.ann.filter_missense_first.vcf

# Usagi

De data uit de pdf files is handmatig in een csv bestand gezet.

Om de data te mappen naar het OMOP Datamodel wilden we Usagi gebruiken. 
We hebben daarvoor vocabulary files van Athena gedownload en deze in usagi geladen.

Dit verliep niet echt soepel, Usagi gaf telkens een error terug waarin stond dat er niet genoeg ruimte was (dit is uiteindelijk wel gelukt).
Hier liepen we vast omdat we niet precies begrepen wat de precies de bedoeling was van het mappen en hoe Usagi precies werkt.

# Database

Het is ons niet gelukt om de data te mappen naar het OMOP CDM.
We zijn wel begonnen aan een python script om verbinding te maken en queries uit te voeren om de data er in te zetten.
Het script is niet compleetomdat we niet echt konden testen met de juiste data, de queries die er in staan werken wel.

# De Workflow

Omdat het via galaxy niet lukte en we daar eigenlijk te lang mee door zijn gegaan zijn we in tijdsnood gekomen.
Dit heeft er toe geleid dat we niet echt een complete workflow kunnen maken, toch hebben we goed kennis gemaakt met workflowmanagers.

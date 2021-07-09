# Werkende applicatie Data Integratie (BI10T-ApD - kans 2)

# Groep 2
- Projectleden
  - Armin van Eldik
  - Jung Ho Loos
  - Rutger Kemperman

# Opdrachtomschrijving
Het doel van het project data-integraty Hyve was het bouwen van een ETL/workflow waarmee input patiënten data (in .VCF format) gemanipuleerd wordt en de output naar een database geparsed wordt. Gedurende het proces moet de input data geannoteerd en gefilterd worden, en vervolgens ook worden gemapt op syntactische en semantische wijze. Uiteindelijk wordt na het mappen de data in de database geplaatst.

# Workflow
- UseGalaxy
  - UseGalaxy is origineel gebruikt om de data in te laden en te annoteren. 
  - De input data (Patiënten .csv files) zijn ingeladen in UseGalaxy en vervolgens gefilterd op chromosoom 21 met bcftools filter 
  - De gefilterde data is vervolgens in SnpEff gepiped om geannoteerd te worden.
  - Handmatig is er gecontroleerd of de data correct geannoteerd was, helaas werkte SnpEff niet in Galaxy.
  - Wegens tekortkomingen in Galaxy is er vervolgens voor gekozen om de workflow uit te werken in bash met python. 

- Bash uitwerking
  - De workflow is vervolgens uitgebreider uitgewerkt in bash.


# Hoe gebruik je de pipeline?
De pipeline bestaat uit een bashscript dat aangeroepen dient te worden vanaf de linux commandline.
-  Commando om de pipeline uit te voeren: $ bash /pipeline.sh
Input: De pipeline bestaat uit .vcf files met patiënten data. 
- De .vcf files bevatten de 8 standaard velden aanwezig in het .vcf file formaat, die informatie over de patiënten beschrijven. Deze velden bevatten:
  - Chromosoom nummer.
  - Positie op het chromosoom.
  - ID, een identifier bijvoorbeeld in dnSNP format. 
  - REF: Het referentie allel. Dit kan ook een groter aantal basen beslaan in het geval van een InDel event.
  - ALT: Het aangepaste allel zoals deze is aangetroffen in de patiënt. Deze komen voor in de vorm van SNPs, InDels, en artefacten. 
  - QUAL: Een PHRED-kwaliteitscore. 
  - FILTER: Definieert of een gemaakte call alle filters heeft doorlopen. In het geval alle filters doorlopen zijn geeft dit een PASS aan, anders wordt de filter die niet gepasseerd is aangegeven in dit veld.  
  - INFO: Dit veld is gevuld met extra informatie omtrent de aangetroffen mutatie. 
- De .vcf files dienen in dezelfde directory te staan als de pipeline.
Output: De output van de pipeline zijn gevulde measurements, person, en condition_occurrence tabellen in de postgres PostgreSQL database.

# Mappen met Usagi
Uiteindelijk is Usagi gebruikt om de patiëntendata uit de vcf files te mappen tegen de SNOMED, gender en race vocabularies verkregen uit Athena. Gezien Usagi een tool met een GUI is, is deze stap handmatig uitgevoerd. In de stappen hieronder staat beschreven hoe het mappen van concept IDs naar de sourcecode is gedaan.
- Stap 1: Als eerste vereist Usagi dat er een index gebuild wordt om het mappen te kunnen uitvoeren. Hiervoor moet de gedownloade vocabulary uitgepakt zijn. Laadt de directory waarin de vocabularies staan in Usagi zodat hiermee de index gebuild kan worden. 
  - Usagi zal dan de index gaan bouwen, sluit wanneer deze hiermee klaar is Usagi af, en start deze vervolgens opnieuw op. 
- Stap 2: De index is gebuild, nu kan er een eigen file ingeladen worden. Ga hiervoor naar File > Import codes, en selecteer een file waarmee gemapt kan worden. 
- Stap 3: Usagi vergelijkt per source de ingeladen filedata met de beschikbare vocabularies en wijst vervolgens automatisch het concept uit de vocabulaire met de hoogste score aan de source data toe. Handmdatig kunnen meerdere concepten toegevoegd worden aan iedere source, dit is niet verplicht.
- Stap 4: Vervolgens dienen deze concepten manueel gecureerd te worden, dit wordt gedaan door de concepten wel of niet goed te keuren. In Usagi kunnen de concepten die toegekend zijn aan de ingeladen sourcedata handmatig gevalideerd worden door op de "Approve" knop te drukken, nu zijn de concepten gemapt naar de source data.
- Stap 5: De concept data kan nu geëxporteerd worden naar een csv file door naar File > Save As... te gaan en de file op te slaan.

# Requirements
Gezien de flow van het project grotendeels plaats vindt in bash zijn er een aantal vereisten voor het script om uitgevoerd te kunnen worden. 

- Linux Ubuntu omgeving versie 18.04 of 20.04
- Samtools moet geïnstalleerd staan (versie 10.2 of nieuwer) (to be verified)
- SnpEff moet geïnstalleerd en sourced zijn (Versie 5.0e of nieuwer)
- De vocabularies gebruikt om te mappen moeten gedownload zijn van Athena:
  - ID 1: OMOP Gender
  - ID 12: Race and ethnicity Code Set (USBC)
  - ID 13: Systemetic Nomenclature of Medicine - Clinical Terms (HTSDO) (SNOMED)
  - ID 139: Human Gene Nomenclature (European Bioinformatics Institute) (HGNC)

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

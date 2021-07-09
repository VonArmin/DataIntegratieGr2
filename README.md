# Werkende applicatie Data Integratie (BI10T-ApD - kans 2)

# Groep 2
Projectleden
- Armin van Eldik
- Jung Ho Loos
- Rutger Kemperman

# Opdrachtomschrijving
Het doel van het project data-integratie Hyve was het bouwen van een ETL/workflow waarmee input patiënten data (in .VCF format) gemanipuleerd wordt en de output naar een database geparsed wordt. Gedurende het proces moet de input data geannoteerd en gefilterd worden, en vervolgens ook worden gemapt op syntactische en semantische wijze. Uiteindelijk wordt na het mappen de data in de database geplaatst. 
- patiënten data van website: https://personalgenomes.ca/data

# Workflow
- UseGalaxy
  - UseGalaxy is origineel gebruikt om de data in te laden en te annoteren. 
  - De input data (Patiënten .csv files) zijn ingeladen in UseGalaxy en vervolgens gefilterd op chromosoom 21 met bcftools filter 
  - De gefilterde data is vervolgens in SnpEff gepiped om geannoteerd te worden.
  - Handmatig is er gecontroleerd of de data correct geannoteerd was, helaas werkte SnpEff niet in Galaxy.
  - Wegens tekortkomingen in Galaxy is er vervolgens voor gekozen om de workflow uit te werken in bash met python. 

- Bash uitwerking
  - De workflow is vervolgens uitgebreider uitgewerkt in bash. Door het bash script aan te roepen voert het automatisch alle stappen uit van .vcf file patiënten data als input tot gemapte data in postgresql tabellen als output. Dit process wordt volledig als een soort van pipeline uitgevoerd met als enige interruptie het toewijzen van concepten aan source data en handmatige controle hierop. 
  - Het proces dat doorlopen wordt door de bashfile is alsvolgt:
    - Door het bash script aan te roepen worden als eerste de locaties (paths) van de patiënten .vcf files opgeslagen in een object voor later gebruik. 
    - Met grep worden uit iedere file alleen de data op chromosoom 21 opgeslagen en naar een output.vcf bestand geparsed.
    - Vervolgens wordt met SnpEff -ann de data geannoteerd, zie hiervoor het onderstaande voorbeeld commando:

    ``` 		java -jar $snpeff GRCh37.75 -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -verbose "${file}_chr21.vcf" > "${file}_ann.vcf" ```
    
    - Deze data is dan geannoteerd. Na het annoteren van de patiënten data wordt deze met SnpSift filter gefilterd op "missense_variant" en "frameshift_variant", dit wordt sequentieel met 2 commando's uitgevoerd. Dit resulteert in 2 files ieder met unieke varianten die bij elkaar gevoegd moeten worden.  
    - Onderstaand het commando voor het filteren op "missense_variant":
    
    ``` java -jar $snpsft filter "ANN[0].EFFECT has 'missense_variant'" "${file}_ann.vcf"  > "${file}_fmiss.vcf" ``` 
    
    - Onderstaand het commando voor het filteren op "frameshift_variant":
    
    ``` java -jar $snpsft filter "ANN[0].EFFECT has 'frameshift_variant'" "${file}_ann.vcf"  > "${file}_fframe.vcf" ``` 
    
    - Deze 2 verschillende varianten files worden uiteindelijk bij elkaar gevoegd met het volgende commando:

    ``` merge "${file}_fmiss.vcf" "${file}_fframe.vcf" "${file}_merged.vcf" ```
    
    - De nu overbodige files worden tussentijds ook verwijderd om ruimte te besparen:
    
    ``` rm -f "${file}_chr21.vcf" "${file}_ann.vcf" "${file}_fmiss.vcf" "${file}_fframe.vcf" ```
    
    - Vervolgens wordt het pythonscript 'extract_versions.py' aangeroepen om 10 random samples uit de gemergede file te halen. Dit wordt gedaan door allereerst de gemergede file te openen, eveneens als een output file, en naar de output file een header weg te schrijven. Vervolgens worden de 10 random samples uit de gemergede file weggeschreven naar de output file. Deze output file is in .csv format zodat deze in Usagi geladen kan worden. Zie hiervoor ook het script. 
    - Usagi wordt vervolgens opgestart en het script wordt tijdelijk gehalt. Nu Usagi geopend is zijn er in Usagi een paar menselijke handelingen vereist om door te kunnen gaan. Zie hiervoor ook het onderstaande kopje Usagi. 
    - Vanuit Usagi is er na de afgelopen stap een file geproduceerd genaamd "conditions.csv". Deze data kan in de tabel gezet worden vervolgens.
    - Usagi wordt gesloten en de pipeline zal zichzelf hervatten. Middels het volgende python script, 'DB_connect.py', wordt de data uit de Usagi file in de bijbehorende tabellen geplaatst. Zie voor de querries het script. 
    - Einde script, de data staat in de tabellen in de OMOP database. Dit kan handmatig geverifieerd worden door de database te querryen.  
    
# Hoe gebruik je de pipeline?
De pipeline bestaat uit een bashscript dat aangeroepen dient te worden vanaf de linux commandline.
-  Commando om de pipeline uit te voeren: $ bash /pipeline.sh
Input: De pipeline bestaat uit .vcf files met patiënten data en een .csv file met informatie over de patienten zelf 
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
- De .csv file bevat 11 colommen die informatie over de patienten zelf beschrijven. Deze colommen zijn:
  - Particpant
  - Birth month
  - Birth year
  - Sex
  - Ethnicity
  - Blood type
  - Blood pressure (mmHg)
  - Weight (kg)
  - Height (cm)
  - Body type 
  - Conditions or Symptom
Output: De output van de pipeline zijn gevulde measurements, person, en condition_occurrence tabellen in de postgres PostgreSQL database.

# Mappen met Usagi
Uiteindelijk is Usagi gebruikt om de patiëntendata uit de vcf files te mappen tegen de SNOMED, gender en race vocabularies verkregen uit Athena. Gezien Usagi een tool met een GUI is, is deze stap handmatig uitgevoerd. In de stappen hieronder staat beschreven hoe het mappen van concept IDs naar de sourcecode is gedaan.
- Stap 1: Als eerste vereist Usagi dat er een index gebuild wordt om het mappen te kunnen uitvoeren. Hiervoor moet de gedownloade vocabulary uitgepakt zijn. Laadt de directory waarin de vocabularies staan in Usagi zodat hiermee de index gebuild kan worden. 
  - Usagi zal dan de index gaan bouwen, sluit wanneer deze hiermee klaar is Usagi af, en start deze vervolgens opnieuw op. 
- Stap 2: De index is gebuild, nu kan er een eigen file ingeladen worden. Ga hiervoor naar "File" > "Import codes", en selecteer een file waarmee gemapt kan worden. 
- Stap 3: Usagi vergelijkt per source de ingeladen filedata met de beschikbare vocabularies en wijst vervolgens automatisch het concept uit de vocabulaire met de hoogste score aan de source data toe. Handmdatig kunnen meerdere concepten toegevoegd worden aan iedere source, dit is niet verplicht.
- Stap 4: Vervolgens dienen deze concepten manueel gecureerd te worden, dit wordt gedaan door de concepten wel of niet goed te keuren. In Usagi kunnen de concepten die toegekend zijn aan de ingeladen sourcedata handmatig gevalideerd worden door op de "Approve" knop te drukken, nu zijn de concepten gemapt naar de source data.
- Stap 5: De concept data kan nu geëxporteerd worden naar een csv file door naar "File" > "Save As..." te gaan en de file op te slaan. Geef deze file de naam "conditions.csv", in het geval de file anders benoemd wordt zal het script stuk lopen. 

# Requirements
De flow van het project vindt grotendeels plaats in bash. Voor het goed uitvoeren van het script zijn een aantal vereisten opgestld.
- Linux Ubuntu omgeving versie 18.04 of 20.04
- Python moet geïnstalleerd staan (versie 3.8 is gebruikt, oudere versies kunnen de flow van de pipeline mogelijk verstoren)
- Java moet geïnstalleerd staan (versie 1.8 of nieuwer, vereist voor Usagi)
- Samtools moet geïnstalleerd staan (versie 10.2 of nieuwer)
- SnpEff moet geïnstalleerd en sourced zijn (Versie 5.0e of nieuwer)
- Usagi moet geïnstalleerd staan (versie 1.4.3)
- De vocabularies gebruikt om te mappen moeten gedownload zijn van Athena:
  - ID 1: OMOP Gender
  - ID 12: Race and ethnicity Code Set (USBC)
  - ID 13: Systemetic Nomenclature of Medicine - Clinical Terms (HTSDO) (SNOMED)
  - ID 139: Human Gene Nomenclature (European Bioinformatics Institute) (HGNC)


# Database
Na het mappen is de data opgeslagen in het OMOP CDM, een postgresql server.
Met een python bestand is connectie gemaakt met de database en is met behulp van querries de data gecommit naar verschillende tabellen.

De data van de patiënten werd uiteindelijk opgeslagen in de tabellen:
- person
- condition_occurrence
- measurement

De Tabel "person" bevat de persoonlijke informatie over de patienten. In de tabel worden de volgende gegevens opgeslagen:
- person_id
- gender_concept_id
- year_of_birth
- month_of_birth
- race_concept_id
- ethnicity_concept_id

De Tabel "condition_occurence" bevat de informatie over de ziektes. In de tabel worden de volgende gegevens opgeslagen:
- condition_occurrence_id
- person_id
- condition_concept_id
- condition_start_date
- condition_type_concept_id
- stop_reason

De Tabel "measurement" zou informatie bevatten over de gekozen varianten, omdat deze niet gemapt konden worden is er als proof of concept andere data in de tabel opgeslagen. In de tabel worden de volgende gegevens opgeslagen:
- measurement_id
- person_id
- measurement_concept_id
- measurement_date
- measurement_type_concept_id


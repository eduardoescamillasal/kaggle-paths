## Data Set Information:
[UCI source](http://archive.ics.uci.edu/ml/datasets/Gas+sensor+array+temperature+modulation)  
[Data folder](http://archive.ics.uci.edu/ml/machine-learning-databases/00487/)

A chemical detection platform composed of **14 temperature-modulated metal oxide semiconductor (MOX) gas sensors** was exposed to dynamic mixtures of carbon monoxide (**CO**) and humid synthetic air in a gas chamber.

The acquired **time series of the sensors** and the measured values of **CO concentration**, **humidity** and **temperature** inside the gas chamber are provided.

- **Chemical detection platform**  
The chemical detection platform was composed of **14 MOX gas sensors** that generate a time-dependent multivariate response to the different gas stimuli.
The utilized sensors were made commercially available by Figaro Engineering (**7** units of **TGS 3870-A04**) and FIS (**7** units of **SB-500-12**).
The operating temperature of the sensors was controlled by the built-in heater, which voltage was modulated in the range **0.2-0.9** V in cycles of **20** and **25** s, following the manufacturer recommendations (**0.9** V for **5** s, **0.2** V for **20** s, **0.9** V for **5** s, **0.2** V for **25** s, ...).
The sensors were **pre-heated for one week** before starting the experiments.
The MOX read-out circuits consisted of voltage dividers with **1** MOhm load resistors and powered at **5** V.
The output voltage of the sensors was sampled at **3.5 Hz** using an **Agilent HP34970A/34901A DAQ** configured at **15** bits of precision and input impedance greater than **10** GOhm.

- **Generator of dynamic gas mixtures**  
Dynamic mixtures of CO and humid synthetic air were delivered from high purity gases in cylinders to a small-sized polytetrafluoroethylene (**PTFE**) test chamber (**250** cm<sup>3</sup> internal volume), by means of a piping system and mass flow controllers (**MFCs**).
Gas mixing was performed using mass flow controllers (**MFC**),which controlled three different gas streams (**CO**, **wet air** and **dry air**). These streams were delivered from high quality pressurized gases in cylinders.
The selected MFCs (**EL-FLOW Select, Bronkhorst**) had full scale flow rates of **1000** mL/min for the dry and wet air streams and **3** mL/min for the CO channel.
The CO bottle contained **1600** ppm of CO diluted in synthetic air with **21 &plusmn; 1%** O<sub>2</sub>.
The relative uncertainty in the generated **CO concentration** was below **5.5%.**
The wet and dry air streams were both delivered from a synthetic air bottle with **99.995%** purity and **21 &plusmn; 1%** O<sub>2</sub>.
Humidification of the wet stream was based on the saturation method using a glass bubbler (**Drechsler** bottles).

- **Temperature/humidity values**  
A temperature/humidity sensor (**SHT75**, from **Sensirion**) provided reference humidity and temperature values inside the test chamber with tolerance below **1.8%** r.h. and **0.5** &deg;C, respectively, every **5** s.
The temperature variations inside the gas chamber, for each experiment, were below **3** &deg;C.

- **Experimental protocol**  
Each experiment consisted on **100** measurements: **10** experimental concentrations uniformly distributed in the range **0-20** ppm and **10** replicates per concentration.
Each replicate had a relative humidity randomly chosen from a uniform distribution between **15%** and **75%** r.h.
At the beginning of each experiment, the gas chamber was cleaned for **15** min using a stream of synthetic air at a flow rate of **240** mL/min.
After that, the gas mixtures were released in random order at a constant flow rate of **240** mL/min for **15** min each.
A single experiment lasted **25** hours (100 samples x 15 minutes/sample) and was replicated on **13** working days spanning a natural period of **17** days.

#### Attribute Information:

The dataset is presented in 13 text files, where each file corresponds to a different measurement day. The filenames indicate the **timestamp (yyyymmdd_HHMMSS)** of the start of the measurements.
Each file includes the acquired time series, presented in 20 columns: 

| Time (s)  | CO concentration (ppm)    | Humidity (%r.h.)  | Temperature (C) | Flow rate (mL/min) |  Heater voltage (V) |
| --------- |:-------------------------:|:-----------------:|:---------------:|:------------------:|:-------------------:|

and the measured resistance of the 14 MOX gas sensors: 

| R01 (MOhm) | R02 (MOhm) | R03 (MOhm) | R04 (MOhm) | R05 (MOhm) | R06 (MOhm) |  R07 (MOhm) |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |  ---------- |


| R08 (MOhm) | R09 (MOhm) | R10 (MOhm) | R11 (MOhm) | R12 (MOhm) | R13 (MOhm) | R14 (MOhm) |
| ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |

Resistance values **R01-R07** correspond to **FIGARO TGS 3870 A-04** sensors, whereas **R08-R14** correspond to **FIS SB-500-12** units.
The time series are sampled at **3.5 Hz**.

**Aquisition module**
  - Agilent HP34970A/34901A DAQ

**Sensors used**
- Sensirion **SHT75**
- FIS **SB-500-12**
- Figaro **TGS 3870-A04**

**Important limitations to note:**
-  MOX sensors lacks selectivity
-  MOX sensors lacks stability
-  MOX sensors have slow recovery time
-  MOX sensors have large tolerances in specifications for identical devices

**Transduction**  
The transduction mechanism of MOX sensors consists on  
measuring resistance changes resulting from chemical interactions  
between the gas species and the metal oxide surface.

**Selectivity**  
Selectivity to a given analyte can be increased by  
modulating the operating temperature with a periodic heating  
power waveform [4]. The resulting multivariate response patterns  
capture the selectivity-temperature dependence characteristic of  
the target gas plus the effect of the interferences. The variables of  
the response pattern are highly correlated because the shape of the  
heating waveform smoothly varies the sensor temperature (except  
for the temperature transitions).

![Block diagram of the LOD estimation/validation method](images/lod-estimation.jpg "Figure 1")  
**Figure 1.** Experimental test bench for the generation of dynamic gas mixtures and acquisition of the sensor signals. Left: Block diagram. Right: Picture. [1]

![Block diagram of the LOD estimation/validation method](images/sensor.png "Figure 2")  
**Figure 2.** Sensor response illustration. [2]

### Exposure due to human inhaling

| Level of CO | Health Effects, and Other Information |
| -----------:|:------------------------------------- |
| 0 PPM | Normal, fresh air. |
| 9 PPM | Maximum recommended indoor CO level (ASHRAE). |
| 10-24 PPM | Possible health effects with long-term exposure. |
| 25 PPM | Max TWA Exposure for 8 hour work-day (ACGIH). Pocket CO TWA warning sounds each hour. |
| 50 PPM | Maximum permissible exposure in workplace (OSHA).First Pocket CO ALARM starts (optional, every 20 seconds). |
| 100 PPM | Slight headache after 1-2 hours. |
| 125 PPM | Second Pocket CO ALARM starts (every 10 seconds). |
| 200 PPM | Dizziness, naseau, fagitue, headache after 2-3 hours of exposure. |
| 400 PPM | Headache and nausea after 1-2 hours of exposure. Life threatening in 3 hours. Third Pocket CO ALARM starts (every 5 seconds). |
| 800 PPM | Headache, nausea, and dizziness after 45 minutes; collapse and unconsciousness after 1 hour of exposure. Death within 2-3 hours. |
| 1000 PPM | Loss of consciousness after 1 hour of exposure. |
| 1600 PPM | Headache, nausea, and dizziness after 20 minutes of exposure. Death within 1-2 hours. |
| 3200 PPM | Headache, nausea, and dizziness after 5-10 minutes; collapse and unconsciousness after 30 minutes of exposure. Death within 1 hour. |
| 6400 PPM | Death within 30 minutes. |
| 12,800 PPM | Immediate physiological effects, unconsciousness. Death within 1-3 minutes of exposure. |


### Analytics approaches suggestion
  1. Threshhold classifier (warning system)
  2. Concentration predictor (advanced logging system)
  3. Concentration classifier (simple logging system)
  4. Substance identifier (monitoring system)

#### Reverences:

The description of the experimental setup and chemical detection platform can be found in [1-2].  
The dataset has been used also in [3].

1. J. Burgués, J.M Jiménez-Soto, S. Marco, *Estimation of the limit of detection in semiconductor gas sensors through linearized calibration models*, Analytica chimica acta 1013 (2018): 13-25.
2. J. Burgués, S. Marco, *Multivariate estimation of the limit of detection by orthogonal partial least squares in temperature-modulated MOX sensors*, Analytica chimica acta 1019 (2018): 49-64.
3. L. Fernandez, J. Yan, J. Fonollosa, J. Burgués, A. Gutierrez, S. Marco, *A practical method to estimate the resolving power of a chemical sensor array: application to feature selection*, Frontiers in chemistry 6 (2018).
30. A.P. Lee, B.J. *Reedy, Temperature modulation in semiconductor gas sensing*, Sensors Actuators B Chem. 60 (1999) 35e42.
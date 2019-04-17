import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output
from textwrap import dedent

import pandas as pd
import plotly.graph_objs as go
import os

from init import app

def create_opts(unique_values):
    cleanlist = [x for x in unique_values if str(x) != 'nan']
    cleanlist.sort()
    cleanlist.insert(0,'All')
    opts = []
    for s in cleanlist:
        val = {'label':s, 'value':s}
        opts.append(val)
    return opts

df = pd.read_csv('data/cities_forecasts.csv')
city_data = pd.read_csv('data/city_data.csv')
city_data = city_data[['City', 'State', 'Grade', 'Hate Crime Trend', 'Notes', 'Crime Data Source']]
city_opts = create_opts(df.city.unique().tolist())
state_opts = create_opts(df.state.unique().tolist())
grade_opts = create_opts(df.grade.unique().tolist())
trend_opts = create_opts(df.trend.unique().tolist())
pop_opts = create_opts(['0-100000','100001-250000','250001-500000','500001-1000000','1000001-5000000','5000001+'])

def aggr_func(groups, count, df):
    df1 = pd.DataFrame(df.groupby(groups)[count].median()).reset_index()
    return df1

explore_layout = dbc.Col([
                        html.H3('Data Exploration Tool', style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto'}),
                        html.P('Below is a visualization tool with which users can explore the data and forecasts collected and \
                        generated in this project. Here are some helpful tips:\
                        ', style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto'}),
                        html.Ul([html.Li('All three graphs are identical and independent copies, presented so users can add \
                        various filters and make comparisons. For example, a user might want to compare A ratings with B and C ratings, respectively. \
                        Users can also compare across cities, states, trends, and population levels.'),
                        html.Li('Users can add multiple filters, but they function similar to an inner join. For instance, if you \
                        select \"Los Angeles\" and \"OH\", the graph will not return any results, as there are no data that Los Angeles and Ohio share. '),
                        html.Li('To undo your filters, select the \"Undo\" button at the bottom left of the page.'),
                        html.Li('The \"Compare to All\" checkbox enables a line that represents all data, for all cities, population \
                        levels, etc. This can be de-selected at any time.'),
                        html.Li('In the upper right hand corner of each graph, you can click on the camera icon to download your \
                        specific selection as a .png file.'),
                        html.Li('Because the data is left-skewed, the trends reflect the medians, not the means.'),
                        html.Li('The seasonal variation in hate crime data is consistent with seasonal variations in crime data \
                        in general.'),
                        html.Li('You can find the municipality data sources used on the Data Sources page.')],
                        style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto'}),
                ])

graph_layout = dbc.Col([
                        html.H3("Monthly Hate Crimes"),
                    dcc.Graph(
                        id='hate-crimes-graph'
                    )
                ])

filters = dbc.Container([
                html.Div([
                    dcc.Checklist(
                        id = 'hate-crimes-compare-all',
                        options= [{'label': 'Compare to All','value':1}],
                        values = [1]
                    )
                ]),
                html.Div([
                    html.Label('City:'),
                    dcc.Dropdown(
                        id='city-select',
                        options=city_opts,
                        value='All',
                        clearable=False
                    ),
                ]),
                html.Div([
                    html.Label('State:'),
                    dcc.Dropdown(
                        id='state-select',
                        options=state_opts,
                        value='All',
                        clearable=False
                    ),
                ]),

                html.Div([
                    html.Label('Grade:'),
                    dcc.Dropdown(
                        id='grade-select',
                        options=grade_opts,
                        value='All',
                        clearable=False
                    )
                ]),

                html.Div([
                    html.Label('Trend:'),
                    dcc.Dropdown(
                        id='trend-select',
                        options=trend_opts,
                        value='All',
                        clearable=False
                    )
                ]),
                html.Div([
                    html.Label('Population:'),
                    dcc.Dropdown(
                        id='pop-select',
                        options=pop_opts,
                        value='All',
                        clearable=False
                    )
                ]),
            ])

abstract_layout = html.Div([
    html.H3('Abstract', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('This project explores the intersection of the risks from doxing and hate crimes.\
    The aim of our work is to highlight the greatest vulnerabilities that exist in data protection\
    for victims, witnesses, or suspects of crimes—specifically, hate crimes—and provide some recommendations\
    from best practices that public officials can implement to close the gap. Because there are no mandated\
    regulations governing the public release of police reports in the US, a wide spectrum of data protection\
    exists from municipality to municipality. We created a data set of 276 municipalities--those with at least\
    100,000 people, and graded each to assess the ease of access to sensitive information about victims,\
    witnesses, or suspects. Then, we conducted a time series forecast to identify hate crime trends for each\
    municipality. Combining the two dimensions quickly spotlights which cities are publicly releasing direct\
    identifiers for victims of crimes and also possess a forecasted increase in hate crimes over the next two\
    years, creating a sense of urgency to close the data vulnerability gap. This information will be shared\
    with local government officials as a catalyst to create reform in the way municipalities share sensitive\
    data with the public.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
])

intro_layout = html.Div([
    html.H3('Introduction', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Project Overview', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('People motivated enough by hate to commit a hate crime have more access than ever before to\
    a potential victim’s home, place of work, and other personal information. This could lead to an \
    increased risk of hate crimes where there is both a growing trend of hate crimes and an increased \
    ability to dox someone. Understanding where this intersection lies is critical to identifying if \
    and where these issues exist. Conversely, identifying best practices can also provide guidance for \
    the municipalities who are missing the mark in terms of victim protection.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('While there are many possible stakeholders, in this project, we are focusing on elected \
    officials in municipalities as primary stakeholders, with police departments and the Federal Bureau \
    of Investigation (FBI) as secondary stakeholders. We assume elected officials will be the most \
    responsive to the optics of either low or heightened risk. Police departments may not have the \
    same priorities, as they often have many crimes to investigate with limited resources. Also, while \
    investigating hate crimes is a priority for the FBI[1], it is a large federal bureaucracy that, \
    by definition, is likely to be more slow-moving than a municipal government. \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Therefore, this product does the following:\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Identifies municipalities in which we are most and least likely to see the greatest\
    risk of hate crimes, combined with a relative ease of doxing'),
    html.Li('Identifies best practices and recommendations for municipalities struggling with this issue'),
    html.Li('Presents an interactive data explorer for stakeholders to explore questions and trends that\
    reflect their own interests and priorities')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Background', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Hate Crimes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('According to the FBI, a hate crime is any traditional offense that is in part or in whole driven \
    by the offender’s bias against a person’s membership in a protected group. These protected groups include \
    race, religion, disability, sexual orientation, ethnicity, gender, and gender identity. While hate and/or \
    bias is not a crime, acting on this in a way that harms others is a crime[2]. \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Hate crimes go beyond harming someone’s person or property in a traditional sense. These crimes \
    violate the victims’ civil rights, in addition to the traditional harm. In the United States, every person, \
    regardless of group, deserves equal treatment from both the government and members of their community. It is \
    this prioritization of upholding civil rights that motivates the FBI’s focus on and prosecution of hate crimes as such[3]. \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Doxing', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Doxing (or doxxing) is a form of online abuse by which one party releases personally identifiable \
    information (PII) and/or sensitive information. This is done for many reasons, all with the intention of harm, \
    but started in the online gaming world[4]. According to the FBI[5], hacking victims and members of the law \
    enforcement community are at an increased risk of being doxed.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('While the FBI report[6] associated doxing risk with prosecution of hacker groups such as Anonymous, \
    we are assuming that because the ability to dox requires less sophistication (depending on data availability), \
    the risk is more widespread now. In fact, cities are faced with a need to balance data transparency with \
    protecting individual privacy[7].\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Levels of Personal Information Identifiability', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Below are various levels that can be used to identify people[8]:\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Direct Identifier: Name, Address, social security number'),
    html.Li('Indirect Identifier: Date of Birth, Zip Code, License Plate, Medical Record Number, IP Address, Geolocation'),
    html.Li('Data Linking to Multiple Individuals: Movie Preferences, Retail Preferences'),
    html.Li('Data Not Linking to Any Individual: Aggregated Census Data, Survey Results'),
    html.Li('Data Unrelated to Individuals: Weather')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('De-Identification and Re-Identification of Personally Identifiable Information', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Anonymization, or de-identification, is a common response to privacy concerns in our digital \
    economy. The way this is done is by removing PII from a dataset. However, because of re-identification, \
    anonymization is not a guarantee of privacy.[9] In fact, Hintze and El Emam find that pseudo-anonymized \
    data is much closer to non-anonymized data than anonymized data.[10]\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Re-identification is where PII that had been anonymized is accurately matched with the original \
    owner or subject. This is often done by combining two or more datasets containing different information \
    about the same or overlapping groups of people. Often, this risk occurs when de-identified data is sold \
    to third parties, which then re-identify the particular individuals.[11][12][13][14]\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('One example of this is seen in Sweeney’s 2002 paper, in which she was able to correctly identify \
    87% of the U.S. population with just zip code, birthdate, and sex.[15] Another example is work by Acqusiti \
    and Gross, in which they were able to predict social security numbers with birthdate and geographic \
    location.[16] Other examples include Kondor, et al., who were able to identify people based on mobility and \
    spatial data. While their study only had a 16.8% success rate after a week, it jumped to 55% after four \
    weeks. With higher frequency data collection, they expected higher success rates in even shorter periods of time.[17]\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('There are four general types of de-identification[18]:\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('Removing Data: According to Health Insurance Portability and Accountability Act (HIPAA), \
    only the first 3 digits of a zip code can be reported.'),
    html.Li('Replacing Data with Codes or Pseudonyms: Using unique identifiers instead of names or social \
    security numbers is not enough. Pseudonyms only work if they cannot be reversed.'),
    html.Li('Adding Statistical Noise'),
    html.Li('Aggregation')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('El Emam presents a de-identification protocol for open data[19]:\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('Classify variables according to direct, indirect, and non-identifiers'),
    html.Li('Remove or replace direct identifiers with a pseudonym'),
    html.Li('Use a k-anonymity method to de-identify the indirect identifiers'),
    html.Li('Conduct a motivated intruder test'),
    html.Li('Update the anonymization with findings from the test'),
    html.Li('Repeat as necessary')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('As Narayanan, et. al. suggest, the true risk of re-identification is not just unknown, \
    but unlikely to be truly unknowable.[20] However, assuming re-identification is always possible \
    (albeit difficult or inconvenient), we can measure the relative ease (or lack thereof) with \
    which re-identification is possible.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Products/Algorithms/Model', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('To assess the combined risk of doxing and hate crimes, we took a mixed-methods approach. \
    Specifically, we compiled a list of all U.S. municipalities with populations above 100,000, per \
    the 2010, 2000, and 1990 census reports[21]. Then, we assessed law enforcement data for each of these \
    to determine the individual risk of doxing. We also used hate crime data from the FBI Data Explorer[22] \
    to create time series models to forecast the trend of hate crimes at the national, state, and, for \
    the municipalities in the dataset, local levels. From there, we assessed the combined risk of both.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('For a more detailed overview, please see the Methodology: Doxing Risk Assessment and the \
    Methodology: Time Series Model pages on this site.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Endnotes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('Federal Bureau of Investigation. (2019). Hate Crimes [Folder]. Retrieved February 10, \
    2019, from https://www.fbi.gov/investigate/civil-rights/hate-crimes'),
    html.Li('ibid.'),
    html.Li('Federal Bureau of Investigation. (2019). Hate Crimes [Folder]. Retrieved February 10, 2019, from \
    https://www.fbi.gov/investigate/civil-rights/hate-crimes'),
    html.Li('Snyder, P., Doerfler, P., Kanich, C., & McCoy, D. (2017). Fifteen minutes of unwanted fame: detecting \
    and characterizing doxing. In Proceedings of the 2017 Internet Measurement Conference on  - IMC \'17 (pp. 432–444). \
    London, United Kingdom: ACM Press. https://doi.org/10.1145/3131365.3131385'),
    html.Li('Federal Bureau of Investigation. (2011, December 18). (U//FOUO) FBI Threat to Law Enforcement From “Doxing” | \
    Public Intelligence [FBI Bulletin]. Retrieved February 3, 2019, from \
    https://publicintelligence.net/ufouo-fbi-threat-to-law-enforcement-from-doxing/'),
    html.Li('ibid.'),
    html.Li('Valenta, Blake. (2017, October 6). How to Open Data While Protecting Privacy. Government Technology. \
    Retrieved from http://www.govtech.com/data/How-to-Open-Data-While-Protecting-Privacy.html'),
    html.Li('Lubarsky, Boris. (2017). Re-Identification of “Anonymized” Data. Georgetown Law Technology Review. \
    Retrieved from https://georgetownlawtechreview.org/re-identification-of-anonymized-data/GLTR-04-2017/'),
    html.Li('Narayanan, A., & Shmatikov, V. (2010). Myths and fallacies of \"personally identifiable information.\" \
    Communications of the ACM, 53(6), 24. https://doi.org/10.1145/1743546.1743558'),
    html.Li('Hintze, Mike, & El Emam, Khaled. (2017). Comparing the Benefits of Pseudonymization and Anonymization Under \
    the GDPR. In Privacy Analytics White Paper. International Association of Privacy Professionals. \
    Retrieved from https://iapp.org/media/pdf/resource_center/PA_WP2-Anonymous-pseudonymous-comparison.pdf'),
    html.Li('Porter, C. C. (2008). De-Identified Data and Third Party Data Mining: The Risk of Re-Identification \
    of Personal Information. Shidler Journal of Law, Commerce & Technology, 5, 1.'),
    html.Li('Narayanan, A., & Shmatikov, V. (2010). Myths and fallacies of \"personally identifiable information.\" \
    Communications of the ACM, 53(6), 24. https://doi.org/10.1145/1743546.1743558'),
    html.Li('Lubarsky, Boris. (2017). Re-Identification of \"Anonymized\" Data. Georgetown Law Technology Review. \
    Retrieved from https://georgetownlawtechreview.org/re-identification-of-anonymized-data/GLTR-04-2017/'),
    html.Li('Center, E. P. I. (2019). EPIC - Re-identification. Retrieved February 2, 2019, \
    from https://epic.org/privacy/reidentification/'),
    html.Li('Sweeney, L. (2002). k-ANONYMITY: A MODEL FOR PROTECTING PRIVACY. International Journal of Uncertainty, \
    Fuzziness and Knowledge-Based Systems, 10(05), 557–570. https://doi.org/10.1142/S0218488502001648'),
    html.Li('Acquisti, A., & Gross, R. (2009). Predicting Social Security numbers from public data. \
    Proceedings of the National Academy of Sciences, 106(27), 10975–10980. https://doi.org/10.1073/pnas.0904891106'),
    html.Li('Kondor, D., Hashemian, B., Montjoye, Y. de, & Ratti, C. (2018). Towards matching user mobility traces in \
    large-scale datasets. IEEE Transactions on Big Data, 1–1. https://doi.org/10.1109/TBDATA.2018.2871693'),
    html.Li('Lubarsky, Boris. (2017). Re-Identification of \"Anonymized\" Data. Georgetown Law Technology Review. Retrieved \
    from https://georgetownlawtechreview.org/re-identification-of-anonymized-data/GLTR-04-2017/'),
    html.Li('El Emam, Khaled. (2016). A de-identification protocol for open data. In Privacy Tech. International Association \
    of Privacy Professionals. Retrieved from https://iapp.org/news/a/a-de-identification-protocol-for-open-data/'),
    html.Li('Narayanan, A., Huey, J., & Felten, E. W. (2016). A Precautionary Approach to Big Data Privacy. In S. Gutwirth, \
    R. Leenes, & P. De Hert (Eds.), Data Protection on the Move (Vol. 24, pp. 357–385). Dordrecht: Springer Netherlands. \
    https://doi.org/10.1007/978-94-017-7376-8_13'),
    html.Li('Bureau, U. C. (n.d.). Decennial Census Datasets. Retrieved April 13, 2019, from \
    https://www.census.gov/programs-surveys/decennial-census/data/datasets.html'),
    html.Li('CDE:: Home. (n.d.). Retrieved April 13, 2019, from https://crime-data-explorer.fr.cloud.gov/')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': '12'}),
])

ts_layout = html.Div([
    html.H3('Predicting Hate Crime Trends: A Time Series Model', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('To identify hate crime trends, we used time series modeling to generate forecasts through 2019, training on hate \
    crime data from the FBI’s Crime Data Explorer.[1][2] Specifically, we modeled a 24-step ahead (two-year) forecast for the U.S. \
    as a whole, as well as for each municipality in our data set. Our projections are for hate crimes overall and hate crimes per capita.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Creating the model presented challenges. For instance, the FBI hate crimes data set has sparsity issues, \
    both in terms of hate crimes not being common everywhere and problems with underreporting. We emphasize and caution \
    the reader that forecasts are only as accurate as the quality and comprehensiveness of historical data, as we are \
    relying on reported hate crimes. That being said, as we are mostly concerned with privacy issues stemming from \
    crimes that were reported, the data set is sufficient for our purposes.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('We used the \"Prophet\" time series model to address these challenges as rigorously as possible. \
    Developed by Facebook Research, we selected this model due to its auto-tuning nature and helper methods that follow \
    the scikit-learn framework (i.e. instantiate, fit, predict methods)[3]. Also, it produces reliable forecasts that are \
    robust to outliers and data sparsity issues. The AutoML nature of Prophet made this efficient to tune and \
    straightforward to program, with only roughly 30 lines of code. Finally, this is an efficient model to train, only \
    taking around 10-15 minutes for 276 cities.[4]\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('While there are several ways to test a time series model, Prophet provides built-in functionality for \
    cross-validation testing. This has been useful, as it provides a way to assess various error statistics, including \
    Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), Mean Absolute Percentage Error \
    (MAPE), and upper/lower confidence interval bounds across train/test splits. Further, by providing output across \
    various error statistics, it provides an additional way to assess confidence in our model.[5] \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('As with any auto-tuning model, the lack of a thorough exploratory data analysis leads to the possibility of \
    sub-optimal parameter tuning choices, over or under-fitting, assumption violations, and other errors that can only \
    be avoided via manual engineering. Given the scale of the dataset that we were working with (276 cities), using an \
    AutoML-enabled time series model was a necessity. Despite these limitations, our model produced forecasts with an \
    MAE low enough for us to assume good model fit for cities with more than 20 hate crimes per year, on average, which \
    amounted to 57 of the 276. We chose MAE as our primary diagnostic metric since we wanted the result to be in the same \
    units as the forecast (hate crime volume) and we did not want to apply an increased penalty to higher magnitude errors \
    as MSE or RMSE do. Forecasts for cities with sparse hate crime data are less reliable, with 95% confidence intervals \
    often on both sides of zero. \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('The output of our model, for the U.S. and each city, includes two years of monthly predictions (y-hat), through \
    the end of 2019. To assess the trends for each municipality, we took the difference between the last two years of \
    historical data, 2016-17, and the two years of forecasted data, 2018-19, to see if hate crimes were likely to be \
    increasing, decreasing, or remaining relatively flat. We then combined this with our Municipality Data Security and \
    Doxing Risk Assessment to generate key insights and recommendations. \
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('To explore the time series output further, see our Data Exploration Tool.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Endnotes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('CDE:: Home. (n.d.). Retrieved April 13, 2019, from https://crime-data-explorer.fr.cloud.gov/'),
    html.Li('The most recent version of the Hate Crimes Explorer documents all reported hate crimes from 1991 to 2017.'),
    html.Li('Prophet. (n.d.). Retrieved March 11, 2019, from http://facebook.github.io/prophet/'),
    html.Li('Taylor, S. J., & Letham, B. (2017). Forecasting at scale (No. e3190v2). PeerJ Inc. \
    https://doi.org/10.7287/peerj.preprints.3190v2'),
    html.Li('ibid.')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': '12'}),
])

dox_layout = html.Div([
    html.H3('Municipality Data Security and Doxing Risk Assessment', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('For this assessment, we cross-referenced hate crimes data from the FBI Crime Data Explorer[1] with U.S. Census \
    data from 2010, 2000, and 1990[2]. We included any city with a population greater than 100,000 at any of the three census \
    points. These allowed us to calculate rough per capita hate crime figures for each city. In total, our data set included \
    286 municipalities. We chose to remove any municipalities from states and territories with policies of not reporting hate \
    crimes, as well as any municipality that had reported zero hate crimes during the 1991-2017 review period. This \
    disqualified five cities in Puerto Rico, as well as Savannah, GA, Macon, GA, Honolulu, HI, Gary, IN, Jackson, MS, \
    and Brownsville, TX, leaving us with a set of 276 cities.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Once we compiled our list of cities, we then assessed each municipality in our data set by its level of \
    protection of personally identifiable information (PII). Through a manual research exercise, we examined whether \
    the municipality 1) made incident data available online at all, and 2) if so, whether the data set contained direct \
    or indirect identifiers, compromising privacy of victims, offenders, witnesses, and/or officers, and if so 3) the \
    inconvenience and anonymity associated with obtaining the data. We then graded each municipality’s online doxing \
    risk according to the following scorecard:\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Table([
        html.Tr([html.Td('A'), html.Td('Fully anonymized/aggregated data, no access to online police reports')]),
        html.Tr([html.Td('A-'), html.Td('Fee-based online access to police reports')]),
        html.Tr([html.Td('B+'), html.Td('Mostly anonymized data - i.e. incident address included, but anonymized to the block')]),
        html.Tr([html.Td('B'), html.Td('No online data/reports only available to verified parties in the case')]),
        html.Tr([html.Td('B-'), html.Td('In-person only access to police reports')]),
        html.Tr([html.Td('C+'), html.Td('Exact incident addresses shown, but not full report')]),
        html.Tr([html.Td('C'), html.Td('Full reports available for free with sign-in, or other possibly anonymous online request')]),
        html.Tr([html.Td('C-'), html.Td('Direct identifiers for suspects, not for victims/witnesses')]),
        html.Tr([html.Td('D+'), html.Td('Direct identifier shown for victim/full direct reports available with sensitive cases withheld')]),
        html.Tr([html.Td('D'), html.Td('Recent data (1-2 months) available with direct victim identifiers')]),
        html.Tr([html.Td('D-'), html.Td('Free, full access with direct identifiers with partial information provided')]),
        html.Tr([html.Td('F'), html.Td('Free, full access with direct identifiers')])],
    style={'width': '50%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('This data is accessible in two ways. First, the entire data set, along with sources, can be found on \
    the Results: All Cities page. Second, users can explore this data visually with the data exploration tool.\
    ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Endnotes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('CDE:: Home. (n.d.). Retrieved April 13, 2019, from https://crime-data-explorer.fr.cloud.gov/'),
    html.Li('Bureau, U. C. (n.d.). Decennial Census Datasets. Retrieved April 13, 2019, \
    from https://www.census.gov/programs-surveys/decennial-census/data/datasets.html')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': '12'}),
])

allcities_layout = html.Div([
    html.H3('All Cities'),
    html.Div([
        dt.DataTable(id='my-datatable',
        columns=[{'name': i, 'id': i} for i in city_data.columns],
        data = city_data.to_dict('rows'),
        style_table={'overflowX': 'scroll'},
        style_cell={
            'text-align': 'left',
            'minWidth': '0px', 'maxWidth': '220px',
            'whiteSpace': 'normal'
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        )
    ]),
    html.Div(id='allcities-content'),
])

key_layout = html.Div([
    html.H3('Key Insights', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Of the 276 municipalities in our data set, there was a wide spectrum of data protection and accessibility standards \
    in place. From a standpoint of protecting personally identifiable information (PII), the municipalities where record requests \
    must be submitted in person with proof of being an involved party in the incident were classified as having the most secure \
    policies. It is likely that many municipalities possess these standards due to a lack of budget, technical sophistication, \
    or both, rather than being motivated by data protection goals. On the other extreme, cities like Dallas, TX, provide instant, \
    no-charge, online access to direct identifiers for victims of crimes to anyone who submits an incident identification value \
    into the query interface. A disclaimer on the Dallas police portal states that the ease of access to this sensitive information \
    is an example of the department’s commitment to fostering transparency with the public. From a doxing standpoint, this level \
    of data access and disclosure is an egregious violation of common-sense PII protection standards. Would-be criminals could \
    quickly, easily, and anonymously obtain information that would allow them to re-victimize those who had already been the targets \
    of hate crimes (or any crime, for that matter).', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('The Good', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Cities within the \"A\" grade category demonstrate most reasonable balance between data accessibility and protection \
    against re-identification of involved parties in police reports. Police reports are available via an online medium, usually \
    associated with a fee. Incident data that is publicly available for free is without direct identifiers and at least partially \
    anonymized. Some notable cities that possess grades in this category are New York, NY, Los Angeles, CA, and Philadelphia, PA.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('The Bad', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Direct identifiers provide nefarious actors with the most basic technological competency the ability to successfully \
    dox exposed parties. Although we prioritize the threat of victim and witness doxing above that of suspects, it is still \
    unacceptable for municipalities to leave suspects vulnerable by exposing their PII to the public. If for no other reason, \
    suspects’ sensitive data should also be protected due to the principle that defendants are presumed innocent until proven \
    guilty beyond a reasonable doubt. Municipalities with a grade of \"C-\" have been shown to expose direct identifiers for suspects. \
    Some notable examples of cities with \"C-\" grades are Miami, FL, Madison, WI, and Glendale, CA.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('The Ugly', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('The most egregious violators of common sense data protection policies are those cities who expose direct identifiers of \
    victims, putting them at significant risk for doxing. These are cities who possess a grade of \"D+\" or below. Municipalities that \
    receive a rating of \"D-\" and \"F\" provide full names and home addresses for the victims of reported crimes, often for free and \
    with the ability to access the data anonymously. A short list of notable cities in this category are Dallas, TX, Indianapolis, IN, \
    and Austin, TX.  ', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('On Hate Crime Reporting', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('In order to craft effective mitigation policies to stem the frequency of hate crime, an accurate and comprehensive \
    corpus of hate crime data must exist so that analysts can better understand its prevalence, location, and nature. Unfortunately, \
    our understanding of the issue is only as good as the data provided by local law enforcement agencies to the FBI, who only \
    provide such data voluntarily, since there is no federal mandate. It is no surprise, then, that the FBI shows roughly 6,100 \
    hate crimes per year across the nation, but a Department of Justice survey estimates the number to be closer to 250,000 per \
    year[1]. Many reasons contribute to this massive under-representation of the facts about hate crimes. For one, it is estimated \
    that more than one-half of hate crimes are never formally reported to the police.[2] Further, local police officers are not \
    well-trained to identify and report hate crimes.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('It would be unreasonable to recommend that the FBI take on responsibility for governing hate crime reporting down to a \
    local law enforcement agency level, given there were more than 30,000 law enforcement agencies in the US in 2016.[3] A more \
    scalable method of governance may be to work with whichever governing body oversees the accreditation of local police \
    departments in each state, usually affiliated with the Department of State’s office, to facilitate some sort of centralized \
    oversight into hate crime reporting. Perhaps, the Department of Justice could lobby hard for each state governing body to add \
    a new hate crime identification and reporting training to the accreditation criteria. Any police department that does not have \
    a certain percentage of its force trained within 12 months loses accreditation. The Department of Justice could develop the \
    curriculum, training materials, and funding for the state agencies to utilize. Although not a perfect solution, this would \
    ensure that each department at least has some officers that are well-trained in hate crime identification and reporting.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('On Data Protection', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('While understanding the importance of a police department’s desire to foster a sense of trust through transparency \
    by making police reports available, there must be some common-sense data protection policies in place to prevent the \
    exploitation of those listed in official police records. At the very minimum, direct identifiers associated with any involved \
    parties must be redacted from publicly available police records. Ideally, police reports are only made available to \
    individuals who have been validated as an involved party to the incident. Any data that is released publicly should be \
    aggregated and either void of indirect identifiers or with K-anonymized indirect identifiers.[4]', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('A policy that might serve as a deterrent to malicious attempts to re-identify individuals from public data would be \
    to criminalize such activity at the federal level, as many European countries have done. The Federal Trade Commission has \
    recently noted the lack of any central government policy regarding the management of re-identification risk in public \
    datasets and the potential of problems to occur as a result.[5] This lack of policy is somewhat surprising, given the \
    detailed recommendations put forward in 2012 by the Computer Security Division of the National Institute on Standards \
    and Technology. Moreover, entities as large as Australia[6] and the United Kingdom[7] have legislation that criminalizes \
    re-identification from public datasets in the absence of a demonstrated public good or other legal, needful purpose \
    (e.g., academic research). It is not the case that the importance of dealing with issues related to re-identification \
    in public datasets, including government-curated datasets, is unknown. The U.S. government has simply failed to act in \
    meaningful way in response to the known threat when it comes to hate crime data. The federal government should consider \
    legislation similar to that of other countries, whereby the structure of publicly available data is regulated and \
    re-identification of crime victims without legitimate need-to-know is criminalized.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Directions for Future Research', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Given the importance of possessing comprehensive hate crime reporting data, any methodologies aimed at increasing \
    the frequency of hate crime reporting should be a research focus. Interventions at the local police department level seem \
    to be one of the most direct methods to increase hate crime reporting, short of legislation. Research focused on the \
    effectiveness of different content and delivery media (e.g. seminars, wallet cards, etc.) could have a positive effect \
    on the training void that exists with police officers at the local level.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Endnotes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('Documenting Hate - ProPublica. (2019, April 12). Retrieved from \
    https://projects.propublica.org/graphics/hatecrimes'),
    html.Li('Confusion, Fear, Cynicism: Why People Don’t Report Hate Incidents. (2017, July 31). Retrieved from \
    https://www.propublica.org/article/confusion-fear-cynicism-why-people-dont-report-hate-incidents'),
    html.Li('National Sources of Law Enforcement Employment Data. (2016, October 4). U.S. Department of Justice Office \
    of Justice Programs Bureau of Justice Statistics. Retrieved from https://www.bjs.gov/content/pub/pdf/nsleed.pdf'),
    html.Li('El Emam, Khaled. (2016). A de-identification protocol for open data. In Privacy Tech. International Association \
    of Privacy Professionals. Retrieved from https://iapp.org/news/a/a-de-identification-protocol-for-open-data/'),
    html.Li('Cranor, L. (2016). Open police data re-identification risks. Federal Trade Commission. Retrieved from \
    https://www.ftc.gov/news-events/blogs/techftc/2016/04/open-police-data-re-identification-risks'),
    html.Li('Phillips, M., Dove, E. S., & Knoppers, B. M. (2017). Criminal prohibition of wrongful re‑identification: \
    Legal solution or minefield for big data? Journal of Bioethical Inquiry, 14(4), 527-539. doi:10.1007/s11673-017-9806-9 '),
    html.Li('Data Protection Act 2018, c.12, s.171, s.172. http://www.legislation.gov.uk/ukpga/2018/12/pdfs/ukpga_20180012_en.pdf.')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': '12'}),
])

rec_layout = html.Div([
    html.H3('Recommendations', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Recommendations for Grade A municipalities:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('High Priority Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('None - this is the sweet spot')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Ideal Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Create an authentication method to ensure that those requesting official police records are involved \
    parties to the incident'),
    html.Li('K-anonymize all indirect identifiers (including incident block) in public facing data[1]')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Recommendations for Grade B municipalities:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('High Priority Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('PDF Request - Provide electronic access to a PDF records request form that can be printed and mailed; \
    attach a fee to the request')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Pros:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Provides a reasonable avenue for people lawfully seeking official police records, but face an unreasonable \
    hardship to submitting a request in person'),
    html.Li('Authentication method could still be implemented to ensure that the requestor is a verified party in the case before \
    releasing information to them'),
    html.Li('Does not require additional IT budget/resources/support/maintenance'),
    html.Li('Fees would generate marginal revenue for the city/county, while creating a small barrier to those seeking information \
    unlawfully')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Cons:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Authentication method may not be as rigorous, since requests can be submitted digitally and requestors do not \
    have to physically present themselves to the approving authority'),
    html.Li('Does not automatically generate digital documentation of the request, correspondence, and fulfillment')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Ideal Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Online Form Submission - Create an online portal that allows official police record requests to be submitted \
    digitally; request form can be behind a paywall')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Pros:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Provides a more reasonable level of access for people who are lawfully seeking official police records, but \
    face unreasonable hardship in submitting a request in person (due to proximity, physical disability, lack of transportation, etc.)'),
    html.Li('Enhances accountability by automatically generating digital documentation of the request, correspondence, and fulfillment'),
    html.Li('Authentication method could still be implemented to ensure that the requestor is a verified party in the case before \
    releasing information to them'),
    html.Li('Fees would generate marginal revenue for the city/county while creating a small barrier to those seeking information \
    unlawfully')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Cons:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Most resource intensive - Requires IT budget/resources/support/ maintenance that may be out of reach for cash \
    strapped municipalities'),
    html.Li('Authentication method may not be as rigorous, since requests can be submitted digitally and requestors do not have to \
    physically present themselves to the approving authority')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Recommendations for Grade C municipalities:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('High Priority Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Remove all direct identifiers for suspects from publicly facing data'),
    html.Li('Remove exact incident addresses and any other indirect identifiers from publicly facing data; anonymize to the block, \
    at least')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Ideal Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Attach a fee to police record requests that must be paid via credit/debit card; creates an additional barrier \
    for those seeking information unlawfully, creates a digital accountability trail, creates marginal revenue for the city/county'),
    html.Li('Create an authentication method to ensure that those requesting official police records are involved parties to the \
    incident'),
    html.Li('K-anonymize all indirect identifiers (including incident block) in public facing data[2]')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H4('Recommendations for Grade D and F municipalities:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('High Priority Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Remove all direct identifiers from publicly facing data'),
    html.Li('Remove unfettered public access to full police reports'),
    html.Li('Remove exact incident addresses and any other indirect identifiers from publicly facing data; anonymize to the block, \
    at least')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Ideal Changes:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Attach a fee to police record requests that must be paid via credit/debit card; creates an additional barrier \
    for those seeking information unlawfully, a digital accountability trail, and marginal revenue for the city/county'),
    html.Li('Create an authentication method to ensure that those requesting official police records are involved parties to the \
    incident'),
    html.Li('K-anonymize all indirect identifiers (including incident block) in public facing data[3]'),
    html.Li('Link to LexisNexis Community Crime Map, CrimeMapping.com, or CrimeReports.com')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Endnotes', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ol([html.Li('El Emam, Khaled. (2016). A de-identification protocol for open data. In Privacy Tech. International \
    Association of Privacy Professionals. Retrieved from https://iapp.org/news/a/a-de-identification-protocol-for-open-data/'),
    html.Li('ibid.'),
    html.Li('ibid.')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto', 'font-size': '12'}),
])

bio_layout = html.Div([
    html.H3('Authors', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Mary C. Boardman, PhD', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Mary Boardman is currently a data scientist at PatientPop and has been teaching analytic methods at the University \
    of South Florida since 2015. She transitioned to data science from academia to inform data-driven decision making on a \
    practical level.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('Zach Day', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('Zach comes to the data science field following experience in U.S. Army Intelligence and marketing analytics at \
    Salesforce, where he is currently employed. He plans on using his new data science skills to focus on addressing issues \
    related to climate change.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.H5('John Pette', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('John Pette turned to data science due to an insatiable curiosity about the world and need to learn how things \
    work. He worked for over 13 years as a diplomat and internal management consultant with the U.S. Department of State. \
    He has lived in four countries and visited over 30.', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
])

ack_layout = html.Div([
    html.H3('Acknowledgements', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.P('The team would like to thank the following people who provided support and/or guidance along the way:', style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Ul([html.Li('Our spouses, for being endlessly supportive and understanding of us throughout our UC Berkeley MIDS journeys'),
    html.Li('Alberto Todeschini and Puya Vahabi, our Capstone instructors, UC Berkeley School of Information'),
    html.Li('Nathan Good, UC Berkeley School of Information'),
    html.Li('Joe Hall, Center for Democracy & Technology'),
    html.Li('Natasha Duarte, Center for Democracy & Technology'),
    html.Li('Greg Nojeim, Center for Democracy & Technology'),
    html.Li('Hannah Quay-de la Vallee, Center for Democracy & Technology'),
    html.Li('Dave Maass, Electronic Frontier Foundation'),
    html.Li('Mike Masnick, Floor64/Techdirt')],
    style={'width': '80%', 'margin-left': 'auto', 'margin-right': 'auto'}),

])

@app.callback(
    Output('hate-crimes-graph', 'figure'),
    [Input('hate-crimes-compare-all', 'values'),
     Input('city-select', 'value'),
     Input('state-select','value'),
     Input('grade-select','value'),
     Input('trend-select','value'),
     Input('pop-select','value')])

def update_figure(compare_all_list, selected_city, selected_state, selected_grade, selected_trend, selected_pop):
    filtered_df = df.copy()
    cohort_name = ''
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city']==selected_city]
        cohort_name = cohort_name + 'City:' + selected_city.upper() + ' '
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['state']==selected_state]
        cohort_name = cohort_name + 'State (median):' + selected_state.upper() + ' '
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['grade']==selected_grade]
        cohort_name = cohort_name + 'Grade (median):' + selected_grade.upper() + ' '
    if selected_trend != 'All':
        filtered_df = filtered_df[filtered_df['trend']==selected_trend]
        cohort_name = cohort_name + 'Trend (median):' + selected_trend.capitalize() + ' '
    if selected_pop != 'All':
        cohort_name = cohort_name + 'Population (median):' + selected_pop.capitalize() + ' '
        alist = selected_pop.split('-')
        if len(alist)==1:
            a = int(''.join(i for i in alist[0] if i.isdigit()))
            filtered_df = filtered_df[filtered_df['population']==a]
        else:
            a1 = int(alist[0])
            a2 = int(alist[1])
            filtered_df = filtered_df[(filtered_df['population']>=a1)&(filtered_df['population']<=a2)]
    filtered_df = aggr_func('ds','yhat', filtered_df)
    full_df = aggr_func('ds','yhat', df)

    trace1 = go.Scatter(
        x=filtered_df['ds'], 
        y=filtered_df['yhat'], 
        mode='lines',
        name='Filtered Results',
        text=[cohort_name],
        textposition='top center')

    trace2 = go.Scatter(
        x=full_df['ds'], 
        y=full_df['yhat'], 
        mode='lines',
        name = 'All (median)')

    if len(compare_all_list)==1:
        traces = [trace1, trace2]
    else:
        traces = [trace1]

    return {
        'data': traces,
        'layout': go.Layout(
            title=cohort_name,
            xaxis={'title': 'Year'},
            yaxis={'title': 'Total Monthly Hate Crimes'},
        )
    }

# Data Jobs Dashboard w/ Power BI

## Interactive Version

Due to Power BI Service licensing limitations, the interactive version is not publicly available. The .pbix file is included in this repository.

Here is a gif showcasing the full dashboard:
![Dashboard gif](/images/Full_Display_Gif.gif)

## Project Overview

This project explores salary trends and job distribution in the data job market using Power BI.

The goal was not only to visualize the dataset, but to design an intuitive dashboard that allows users to explore compensation, demand, and geographic distribution efficiently.

### Dashboard File
You can find the file for the dashboard here: [`Dashboard_Proyect_01.pbix`](Dashboard_Proyect_01.pbix).  

## My Approach

Instead of focusing only on visuals, I concentrated on:
- Keeping the layout clean and minimal
- Reducing visual clutter
- Making the KPIs immediately readable
- Structuring the dashboard for fast decision-making

This project helped me better understand filter context, drill-through behavior, and interactive design in Power BI.

## Skills & Techniques Applied

-   **⚙️ Data Transformation (ETL) with Power Query:** Cleaned, shaped, and prepared the raw data for analysis by handling blanks, changing data types, and creating new columns.
-   **🧮 Implicit Measures:** Formulated measures to derive key insights and KPIs like `Median Yearly Salary` and `Job Count`.
-   **📊 Core Charts:** Utilized **Column, Bar, Line,** and **Area Charts** to compare job counts and track trends over time.
-   **🗺️ Geospatial Analysis:** Leveraged **Map Charts** to visualize the global distribution of jobs.
-   **🔢 KPI Indicators & Tables:** Used **Cards** to display key metrics and **Tables** to provide granular, sortable data.
-   **🎨 Dashboard Design:** Designed an intuitive and visually appealing layout, exploring both common and uncommon chart types to best tell the data story.
-   **🖱️ Interactive Reporting:**
    -   **Slicers:** To dynamically filter the report by Job Title.
    -   **Buttons & Bookmarks:** To create a seamless navigation experience.
    -   **Drill-Through:** To navigate from a high-level summary to a contextual, detailed view.
---

## Lessons Learned

- The importance of controlling data types in Power Query
- How visual interactions can unintentionally affect KPIs
- When to use drill-through versus slicers
- Why less visual noise improves dashboard clarity

## Dashboard Overview

*This report is split into two distinct pages to provide both a high-level summary and a detailed analysis.*

### Page 1: High-Level Market View

![Data Jobs Dashboard Page 1](/images/Page_01.png)  

This is your mission control for the data job market. It showcases key KPIs like total job count, median salaries, and top job titles to give you a quick understanding of what's happening in the job market at a glance.

### Page 2: Job Title Drill Through

![Data Jobs Dashboard Page 2](/images/Page_02.png)  

This is the deep-dive page. From the main dashboard, you can drill through to this view to get specific details for a single job title, including salary ranges, work-from-home stats, top hiring platforms, and a global map of job locations.

---

## Conclusion

This dashboard showcases how Power BI can transform raw job posting data into a powerful tool for career analysis. It allows users to slice, filter, and drill through data to make informed decisions about their career paths.
from discord import SelectOption

x = [
    {
        "value": "Aerospace",
        "label": "Aerospace",
        "customProperties": {}
    },
    {
        "value": "Agricultural",
        "label": "Agricultural",
        "customProperties": {}
    },
    {
        "value": "Architecture",
        "label": "Architecture",
        "customProperties": {}
    },
    {
        "value": "AI",
        "label": "AI",
        "customProperties": {}
    },
    {
        "value": "Biomedical",
        "label": "Biomedical",
        "customProperties": {}
    },
    {
        "value": "Biotechnology",
        "label": "Biotechnology",
        "customProperties": {}
    },
    {
        "value": "Textile Technology",
        "label": "Textile Technology",
        "customProperties": {}
    },
    {
        "value": "Ceramic",
        "label": "Ceramic",
        "customProperties": {}
    },
    {
        "value": "Chemical",
        "label": "Chemical",
        "customProperties": {}
    },
    {
        "value": "Chemistry(Bsc/Msc)",
        "label": "Chemistry(Bsc/Msc)",
        "customProperties": {}
    },
    {
        "value": "Civil",
        "label": "Civil",
        "customProperties": {}
    },
    {
        "value": "Computational",
        "label": "Computational",
        "customProperties": {}
    },
    {
        "value": "CSE",
        "label": "CSE",
        "customProperties": {}
    },
    {
        "value": "EEE",
        "label": "EEE",
        "customProperties": {}
    },
    {
        "value": "Instrumentation",
        "label": "Instrumentation",
        "customProperties": {}
    },
    {
        "value": "Electrical",
        "label": "Electrical",
        "customProperties": {}
    },
    {
        "value": "ECE",
        "label": "ECE",
        "customProperties": {}
    },
    {
        "value": "Electronics",
        "label": "Electronics",
        "customProperties": {}
    },
    {
        "value": "Energy",
        "label": "Energy",
        "customProperties": {}
    },
    {
        "value": "Engineering Physics",
        "label": "Engineering Physics",
        "customProperties": {}
    },
    {
        "value": "Food Process Engineering",
        "label": "Food Process Engineering",
        "customProperties": {}
    },
    {
        "value": "Industrial Production",
        "label": "Industrial Production",
        "customProperties": {}
    },
    {
        "value": "Industrial",
        "label": "Industrial",
        "customProperties": {}
    },
    {
        "value": "IT",
        "label": "IT",
        "customProperties": {}
    },
    {
        "value": "Integrated B. Tech.(IT) and M. Tech (IT) (5 Years, Integrated B. Tech. and M. Tech.)",
        "label": "Integrated B. Tech.(IT) and M. Tech (IT) (5 Years, Integrated B. Tech. and M. Tech.)",
        "customProperties": {}
    },
    {
        "value": "Integrated B. Tech.(IT) and MBA (5 Years, Integrated B. Tech. and MBA)",
        "label": "Integrated B. Tech.(IT) and MBA (5 Years, Integrated B. Tech. and MBA)",
        "customProperties": {}
    },
    {
        "value": "Life Science",
        "label": "Life Science",
        "customProperties": {}
    },
    {
        "value": "Material Science",
        "label": "Material Science",
        "customProperties": {}
    },
    {
        "value": "Mathematics and Computing",
        "label": "Mathematics and Computing",
        "customProperties": {}
    },
    {
        "value": "ME",
        "label": "ME",
        "customProperties": {}
    },
    {
        "value": "Mechatronics",
        "label": "Mechatronics",
        "customProperties": {}
    },
    {
        "value": "Metallurgy",
        "label": "Metallurgy",
        "customProperties": {}
    },
    {
        "value": "Mining",
        "label": "Mining",
        "customProperties": {}
    },
    {
        "value": "Physics(Bsc/Msc)",
        "label": "Physics(Bsc/Msc)",
        "customProperties": {}
    },
    {
        "value": "Planning",
        "label": "Planning",
        "customProperties": {}
    },
    {
        "value": "Production",
        "label": "Production",
        "customProperties": {}
    },
    {
        "value": "Quantitative Economics & Data Science (5 Years, Integrated Master of Science)",
        "label": "Quantitative Economics & Data Science (5 Years, Integrated Master of Science)",
        "customProperties": {}
    },
    {
        "value": "Smart Manufacturing (4 Years, Bachelor of Technology)",
        "label": "Smart Manufacturing (4 Years, Bachelor of Technology)",
        "customProperties": {}
    }
]

y = []
for branch in x:
    y.append(f"SelectOption(label={branch['label']})")
    
print(y)
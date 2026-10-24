from django import forms


CITY_CHOICES = [
    ("Bangalore", "Bangalore"),
    ("Hyderabad", "Hyderabad"),
    ("Mumbai", "Mumbai"),
    ("Nagpur", "Nagpur"),
    ("Pune", "Pune"),
]

LOCALITY_TIER_CHOICES = [
    ("Budget", "Budget"),
    ("Mid", "Mid"),
    ("Premium", "Premium"),
]

FURNISHING_CHOICES = [
    ("Semi-Furnished", "Semi-Furnished"),
    ("Unfurnished", "Unfurnished"),
    ("Fully-Furnished", "Fully-Furnished"),
]

YES_NO_CHOICES = [
    ("Yes", "Yes"),
    ("No", "No"),
]


class HousePredictionForm(forms.Form):
    City = forms.ChoiceField(
        choices=CITY_CHOICES,
        initial="Pune",
        required=False,
        label="City",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    Locality_Tier = forms.ChoiceField(
        choices=LOCALITY_TIER_CHOICES,
        initial="Mid",
        required=False,
        label="Locality Tier",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    BHK = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        label="Bedrooms (BHK)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 2",
        }),
    )

    Bathrooms = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=2,
        label="Bathrooms",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 2",
        }),
    )

    Super_Area_sqft = forms.FloatField(
        min_value=1,
        initial=1000.0,
        label="Super Area (sq. ft.)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 1000",
        }),
    )

    Carpet_Area_sqft = forms.FloatField(
        min_value=1,
        initial=800.0,
        required=False,
        label="Carpet Area (sq. ft.)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 800",
        }),
    )

    Floor_No = forms.IntegerField(
        min_value=0,
        initial=3,
        label="Floor Number",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 3",
        }),
    )

    Total_Floors = forms.IntegerField(
        min_value=1,
        initial=10,
        required=False,
        label="Total Floors in Building",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 10",
        }),
    )

    Property_Age_years = forms.IntegerField(
        min_value=0,
        initial=5,
        label="Property Age (years)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 5",
        }),
    )

    Furnishing = forms.ChoiceField(
        choices=FURNISHING_CHOICES,
        initial="Semi-Furnished",
        required=False,
        label="Furnishing Status",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    Parking = forms.ChoiceField(
        choices=[
            ("Yes", "Available"),
            ("No", "Not available"),
        ],
        initial="Yes",
        required=False,
        label="Parking",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    Lift = forms.ChoiceField(
        choices=[
            ("Yes", "Available"),
            ("No", "Not available"),
        ],
        initial="Yes",
        required=False,
        label="Lift",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    Gated_Society = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        initial="Yes",
        required=False,
        label="Gated Society",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    Distance_to_Metro_km = forms.FloatField(
        min_value=0.0,
        initial=2.0,
        required=False,
        label="Distance to Metro (km)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 2.0",
            "step": "0.1",
        }),
    )

    Distance_to_CityCenter_km = forms.FloatField(
        min_value=0.0,
        initial=10.0,
        required=False,
        label="Distance to City Center (km)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 10.0",
            "step": "0.1",
        }),
    )

    Nearby_School_km = forms.FloatField(
        min_value=0.0,
        initial=1.5,
        required=False,
        label="Nearby School Distance (km)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 1.5",
            "step": "0.1",
        }),
    )

    Nearby_Hospital_km = forms.FloatField(
        min_value=0.0,
        initial=2.0,
        required=False,
        label="Nearby Hospital Distance (km)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 2.0",
            "step": "0.1",
        }),
    )

    Crime_Rate_Index = forms.FloatField(
        min_value=0.0,
        max_value=100.0,
        initial=30.0,
        required=False,
        label="Crime Rate Index (0 - 100)",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. 30.0",
            "step": "0.1",
        }),
    )

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("City"):
            cleaned_data["City"] = "Pune"

        if not cleaned_data.get("Locality_Tier"):
            cleaned_data["Locality_Tier"] = "Mid"

        if not cleaned_data.get("Furnishing"):
            cleaned_data["Furnishing"] = "Semi-Furnished"

        if not cleaned_data.get("Parking"):
            cleaned_data["Parking"] = "Yes"

        if not cleaned_data.get("Lift"):
            cleaned_data["Lift"] = "Yes"

        if not cleaned_data.get("Gated_Society"):
            cleaned_data["Gated_Society"] = "Yes"

        super_area = cleaned_data.get("Super_Area_sqft")
        carpet_area = cleaned_data.get("Carpet_Area_sqft")
        if super_area and not carpet_area:
            cleaned_data["Carpet_Area_sqft"] = round(super_area * 0.78, 2)

        floor_no = cleaned_data.get("Floor_No") or 0
        if not cleaned_data.get("Total_Floors"):
            cleaned_data["Total_Floors"] = int(floor_no) + 1

        if cleaned_data.get("Distance_to_Metro_km") is None:
            cleaned_data["Distance_to_Metro_km"] = 2.0

        if cleaned_data.get("Distance_to_CityCenter_km") is None:
            cleaned_data["Distance_to_CityCenter_km"] = 10.0

        if cleaned_data.get("Nearby_School_km") is None:
            cleaned_data["Nearby_School_km"] = 1.5

        if cleaned_data.get("Nearby_Hospital_km") is None:
            cleaned_data["Nearby_Hospital_km"] = 2.0

        if cleaned_data.get("Crime_Rate_Index") is None:
            cleaned_data["Crime_Rate_Index"] = 30.0

        return cleaned_data

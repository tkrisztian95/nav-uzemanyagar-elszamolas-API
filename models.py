class FuelAccountNorm:
    # Initializer / Instance Attributes
    def __init__(self, month, benzin, diesel, mixed, lpg):
        self.month = month.strip()
        self.benzin = benzin.strip()
        self.diesel = diesel.strip()
        self.mixed = mixed.strip()
        self.lpg = lpg.strip()

    def serialize(self):  
        return {           
            'month': self.month, 
            'benzin': self.benzin,
            'diesel': self.diesel,
            'mixed': self.mixed,
            'lpg': self.lpg,
        }
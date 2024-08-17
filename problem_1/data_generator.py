
import random

def generate_random_data(spec, num_records=5):
    """Generate random data based on the spec, using predefined types."""
    types = [
        ['Elizabeth', 'Jonathan', 'Alexander', 'Catherine', 'Isabella'],  # First names
        ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown'],               # Last names
        ['XX', 'YY', 'ZZ'],                                               # Misc values
        ['AB', 'BA'],                                                     # Random 2 chars
        ['NewYork', 'LosAngeles', 'Chicago', 'Houston', 'Phoenix'],       # City names
        '0123456789',                                                     # Numbers
        'XYZabcdef',                                                      # Random chars
    ]
    
    data = []
    for _ in range(num_records):
        record = []
        for i, offset in enumerate(spec['Offsets']):
            field_length = int(offset)
            if i < len(types):
                if isinstance(types[i], list):
                    # Pick a random value from the list
                    field = random.choice(types[i])
                else:
                    # Generate a random string from the allowed characters
                    field = ''.join(random.choices(types[i], k=field_length))
            else:
                # Default fallback to random numbers if no specific type provided
                field = ''.join(random.choices('0123456789', k=field_length))
            
            # Ensure the field strictly matches the length in the spec by padding with spaces if necessary
            field = field.ljust(field_length)[:field_length]
            record.append(field)
        data.append(record)
    return data

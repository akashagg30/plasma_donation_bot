
blood_groups =  ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

blood_group_match = {
    'A+' : ['A+', 'A-', 'O+', 'O-'],
    'A-' : ['A-', 'O-'],
    'B+' : ['B+', 'B-', 'O+', 'O-'],
    'B-' : ['B-', 'O-'],
    'AB+' : ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    'AB-' : ['AB-', 'A-', 'B-', 'O-'],
    'O+' : ['O+', 'O-'],
    'O-' : ['O-'],
}
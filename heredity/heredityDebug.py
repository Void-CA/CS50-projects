import csv
import itertools
import sys
import random

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]






        

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    total_trait = 0
    total_gen = 0
    for x in probabilities:
        person = probabilities[x]
        total_gen = sum([person["gen"][i] for i in person["gen"]])
        total_trait = sum([person["trait"][i] for i in person["trait"]])

        for i in [0,1,2]:
            probabilities[x]["gen"][i] /= total_gen
        
        for i in person["trait"]:
            probabilities[x]["trait"][i] /= total_trait

def joint_probability(people, one_gene, two_genes, have_trait):
    joint_prob = 1.0

    for person in people:
        trait = person in have_trait
        if person in two_genes:
            gen = 2
        elif person in one_gene:
            gen = 1
        else:
            gen = 0

        # Probabilidad del rasgo dado el número de copias del gen
        trait_prob = PROBS["trait"][gen][trait]
        gene_prob = 1.0

        # Probabilidad de herencia del gen
        if people[person]["mother"] is None and people[person]["father"] is None:
            gene_prob = PROBS["gene"][gen]
        else:
            mom = people[person]["mother"]
            dad = people[person]["father"]
            mom_genes = 1 - PROBS['mutation'] if mom in two_genes else 0.5 if mom in one_gene else PROBS["mutation"]
            dad_genes = 1 - PROBS['mutation'] if dad in two_genes else 0.5 if dad in one_gene else PROBS["mutation"]

            if gen == 0:
                gene_prob *= (1 - mom_genes) * (1 - dad_genes)
            elif gen == 1:
                gene_prob *= (1 - mom_genes) * dad_genes + (1 - dad_genes) * mom_genes
            else:
                gene_prob *= mom_genes * dad_genes

        joint_prob *= trait_prob * gene_prob

    return joint_prob

# Datos de las personas
people_data = {
    'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
    'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
    'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

# Calcular la probabilidad conjunta con mensajes de depuración
joint_prob = joint_probability(people_data, {"Harry"}, {"James"}, {"James"})
print(f"Probabilidad Conjunta: {joint_prob}")








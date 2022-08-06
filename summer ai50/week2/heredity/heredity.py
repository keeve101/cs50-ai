import csv
import itertools
from ntpath import join
import sys

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


def joint_probability(people, one_gene, two_genes, have_trait):
    #if parent 2 copies = .99, if parent 1 copy = .50 * .99, if parent 0 copy = .01
    joint_p = 1
    for person, dict in people.items():
        person_trait = True if person in have_trait else False
        person_father = dict["father"]
        person_mother = dict["mother"]

        #one gene
        if person in one_gene:
            p = PROBS["trait"][1][person_trait]
            if person_father:
                if person_father in one_gene:
                    p_father = .5
                    if person_mother in one_gene:
                        p = p * (.5 * .5 * 2)
                    elif person_mother in two_genes:
                        p = p * (p_father * .99 + p_father * .01)
                    else:
                        p = p * (.5 * .99 + .5 * .01)

                elif person_father in two_genes:
                    p_father = .99
                    if person_mother in one_gene:
                        p = p * (p_father * .5 + (1 - p_father) * .5)
                    elif person_mother in two_genes:
                        p = p * (p_father * .01 + (1 - p_father) * .99)
                    else:
                        p = p * (p_father * .99 + (1 - p_father) * .01)
                else:
                    p_father = .01
                    if person_mother in one_gene:
                        p = p * (p_father * .5 + (1 - p_father) * .5)
                    elif person_mother in two_genes:
                        p = p * (p_father * .01 + (1 - p_father) * .99)
                    else:
                        p = p * (p_father * .99 + (1 - p_father) * .01)
            else:
                p = p * PROBS["gene"][1] 
        #two genes
        elif person in two_genes:
            p = PROBS["trait"][2][person_trait]

            if person_father:
                for parent in [person_father, person_mother]:
                    if parent in one_gene:
                        p = p * .5 
                    elif parent in two_genes:
                        p = p * .99 
                    else:
                        p = p * .01 
   
            else:
                p = p * PROBS["gene"][2]

        #zero gene
        else:
            
            if person_father:
                p = PROBS["trait"][0][person_trait]
                for parent in [person_father, person_mother]:
                    if parent in one_gene:
                        p = p * .5 
                    elif parent in two_genes:
                        p = p * .01 
                    else:
                        p = p * .99 

            else:
                p = PROBS["gene"][0] * PROBS["trait"][0][person_trait]

        joint_p = joint_p * p

    return joint_p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person, dict in probabilities.items():
        person_trait = True if person in have_trait else False
        if person in one_gene:
            person_gene = 1
        elif person in two_genes:
            person_gene = 2
        else:
            person_gene = 0
        dict["trait"][person_trait] += p
        dict["gene"][person_gene] += p
    
        

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for dict in probabilities.values():
        gene_sum = sum(dict["gene"].values()) 
        trait_sum = sum(dict["trait"].values()) 
        for i in range(3):
            
            dict["gene"][i] = dict["gene"][i] / gene_sum
        
        for i in range(2):
            dict["trait"][i] = dict["trait"][i] / trait_sum


if __name__ == "__main__":
    main()

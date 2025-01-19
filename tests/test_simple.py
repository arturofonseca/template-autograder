"""Sample test_simple.py file"""

import unittest

from gradescope_utils.autograder_utils.decorators import number, weight

from files.lab2 import *  # will be imported on submission


class TestLab2(unittest.TestCase):
    """Class to test the student's submission."""

    def setUp(self) -> None:
        """Set up the tests.

        Runs before every test.
        """
        self.BREED_FILE_NAME = "files/dog_breed_characteristics.csv"
        self.DOG_FILE_NAME = "files/nyc_dogs.json"

        csvfile = open(self.BREED_FILE_NAME)
        self.breeds = list(csv.reader(csvfile, delimiter=","))
        csvfile.close()

        f = open(self.DOG_FILE_NAME, "r")
        self.dogs = json.load(f)
        f.close()

    @weight(10)
    @number("0")
    def test_load_breeds(self) -> None:
        """Please place a docstring describing what this test is doing."""
        breeds = read_breed_data(self.BREED_FILE_NAME)
        assert isinstance(breeds, list), "breeds should be a list of lists"
        assert isinstance(breeds[0], list), "breeds should be a list of lists"
        assert isinstance(
            breeds[0][1], str
        ), "breeds should be a list of lists of strings"
        assert len(breeds) > 0, "breeds should have at least one entry"
        assert breeds == self.breeds, "Breed data didn't load correctly"

    @weight(10)
    @number("1")
    def test_load_dogs(self) -> None:
        dogs = read_dog_data(self.DOG_FILE_NAME)
        assert len(dogs) > 0, "dogs should have at least one entry"
        assert isinstance(dogs[0], list), "dogs should be a list of lists"
        assert isinstance(dogs[0][1], str), "dogs should be a list of lists of strings"
        assert dogs[2][1] == "SWEETIE", "dog[2][1] should be SWEETIE"
        assert dogs == self.dogs, "Dog data didn't load correctly"

    @weight(10)
    @number("2")
    def test_get_breed_data(self) -> None:
        data = get_breed_data_by_name(self.breeds, "BEAGLE")
        assert isinstance(data, list), "get_breed_data_by_name should return a list"
        assert data[3] == "Scenthound", "Beagle breed data should contain Scenthound"
        data = get_breed_data_by_name(self.breeds, "LABNAPBAP")
        assert (
            data is None
        ), f"LABNAPBAP is not in the data, {data} was returned for it.\nIf there is no data, None should be returned"

    @weight(10)
    @number("3")
    def test_get_breed_data_for_dog(self) -> None:
        data = get_breed_data_for_dog(self.breeds, self.dogs[3])
        assert isinstance(data, list), "get_breed_data_for_dog should return a list"
        assert len(data) == len(
            self.breeds[0]
        ), "get_breed_data_for_dog returned a list of unexpected length"
        assert (
            "Chihuahua" in data
        ), "GIZMO is a Chihuahua and get_breed_data_for_dog should return Chihuahua info when called for GIZMO"

    @weight(10)
    @number("4")
    def test_get_dogs_by_breed(self) -> None:
        beagles_found = get_dogs_by_breed(self.dogs, "beagle")
        assert isinstance(
            beagles_found, list
        ), "test_get_dogs_by_breed should return a list"
        if len(beagles_found) > 0:
            assert isinstance(
                beagles_found[0], list
            ), "test_get_dogs_by_breed should return a list of lists"
        assert (
            len(beagles_found) == 96
        ), f"Testing with Beagle breed, expecting 96 beagles, found {len(data)} beagles"

        labnaps_found = get_dogs_by_breed(self.dogs, "labnap")
        assert (
            len(labnaps_found) == 0
        ), f"Testing with labnap. There should be no labnaps in the data, found {len(labnaps_found)} entries"

    @weight(10)
    @number("5")
    def test_get_names_by_breed(self) -> None:
        beagle_names = get_names_by_breed(self.dogs, "Beagle")
        assert isinstance(
            beagle_names, list
        ), "test_get_dogs_by_breed should return a list"
        assert (
            len(beagle_names) == 96
        ), f"Testing with Beagle, expecting 96 beagles, got {len(beagle_names)} beagles"
        assert "LEYLA" in beagle_names, "Leyla should appear among bealge names"
        assert "BUDDY" in beagle_names, "BUDDY should appear among bealge names"

        labnap_names = get_names_by_breed(self.dogs, "labnap")
        assert (
            len(labnap_names) == 0
        ), f"There should be no labnaps in the data, found {len(labnap_names)} entries"

    @weight(10)
    @number("6")
    def test_has_temperament(self) -> None:
        affenpinscher = self.breeds[1]
        assert has_temperament(
            affenpinscher, "Curious"
        ), "Affenpinscher should have temperament Curious"
        assert not has_temperament(
            affenpinscher, "Friendly"
        ), "Affenpinscher should not have temperament Friendly"
        assert not has_temperament(
            None, "Friendly"
        ), "None should not have temperament Friendly"

        beagle = self.breeds[21]
        assert has_temperament(
            beagle, "Independent"
        ), "Beagle should have temperament Independent"
        assert not has_temperament(
            beagle, "Tenacious"
        ), "Beagle should not have temperament Tenacious"

    @weight(10)
    @number("7")
    def test_get_breeds_by_temperament(self) -> None:
        affectionate_breeds = get_breeds_by_temperament(self.breeds, "Affectionate")
        assert isinstance(
            affectionate_breeds, list
        ), "test_get_breeds_by_temperament should return a list"
        assert (
            len(affectionate_breeds) == 70
        ), "There should be 70 affectionate breeds in this dataset"

        angry_breeds = get_breeds_by_temperament(self.breeds, "Angry")
        assert isinstance(
            angry_breeds, list
        ), "test_get_breeds_by_temperament should return a list"
        assert len(angry_breeds) == 0, "There should be 0 angry breeds in this dataset"

        sweet_breeds = get_breeds_by_temperament(self.breeds, "Sweet")
        assert (
            len(sweet_breeds) == 12
        ), "There should be 12 sweet breeds in this dataset"

    @weight(10)
    @number("8")
    def test_list_all_zip_codes(self) -> None:
        zipcodes = list_all_zip_codes(self.dogs)
        assert isinstance(
            zipcodes, list
        ), "test_list_all_zip_codes should return a list"
        assert (
            len(zipcodes) == 188
        ), f"there are 188 zipcodes in this dataset, you found {len(zipcodes)}"
        assert "10035" in zipcodes, "10035 should be in the zipcodes"
        assert "10128" in zipcodes, "10128 should be in the zipcodes"
        assert "10014" in zipcodes, "One of the zip codes is missing from zipcode list"
        assert (
            zipcodes[-1] == "7733"
        ), f"7733 is the last zipcode in the data set, your code found {zipcodes[-1]}"

    @weight(10)
    @number("9")
    def test_list_breeds(self) -> None:
        test_dogs = self.dogs[0:10]
        test_dog_breeds = list_breeds(test_dogs)
        assert (
            "Pug" in test_dog_breeds
        ), "Pug should be in list of breeds found in this test data"
        assert (
            len(test_dog_breeds) == 8
        ), "8 different breeds should have been found in this test data"

        test_dogs = self.dogs[10:14]
        test_dog_breeds = list_breeds(test_dogs)
        assert (
            "Havanese" in test_dog_breeds
        ), f"Havanese should be in list of breeds found in the following test data {test_dogs}"
        assert (
            "Pekingese" in test_dog_breeds
        ), f"Pekingese should be in list of breeds found in the following test data {test_dogs}"
        assert (
            len(test_dog_breeds) == 4
        ), f"4 different breeds should have been found in this test data: {test_dog_breeds}"

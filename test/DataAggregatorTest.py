import unittest
from Config import Config
from Result import Result
from Aggregation import Aggregation
from DataAggregator import DataAggregator

#------METHODS BEING TESTED--------
#validResults()
#validArray()
#validPercents()
#averagePercent()
#total()
#populateNames()
#parseData()
#sort()

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config()
        self.validURL = self.config.getTwentyone()
        self.results = []

        self.results.append(Result(1, "Matt", "Armen", self.validURL, 90, 70, 20))
        self.results.append(Result(1, "Matt", "Sam", self.validURL, 80, 43, 77))
        self.results.append(Result(1, "Armen", "Sam", self.validURL, 12, 10, 8))
        self.results.append(Result(2, "Matt", "Armen", self.validURL, 33, 70, 45))
        self.results.append(Result(2, "Matt", "Sam", self.validURL, 16, 17, 15))
        self.results.append(Result(2, "Armen", "Sam", self.validURL, 50, 34, 5))
        self.results.append(Result(3, "Matt", "Armen", self.validURL, 76, 79, 20))
        self.results.append(Result(3, "Matt", "Sam", self.validURL, 90, 88, 100))
        self.results.append(Result(3, "Armen", "Sam", self.validURL, 10, 6, 2))

        self.ag = DataAggregator(self.results)
        self.names = self.ag.populateNames(self.results)

#
# validResults()
#
    # Results should be an array of Result
    def test_isValidResults(self):
        self.assertTrue(self.ag.validateResults(self.results))

    # Results should not be empty
    def test_isEmptyResults(self):
        results = []
        self.assertFalse(self.ag.validateResults(results))

#
# validArray()
#
    # Array should not be empty
    def test_arrayEmpty(self):
        percents = []
        self.assertFalse(self.ag.validateArray(percents))

    # Array should have values
    def test_arrayExists(self):
        percents = [1, 2, 3]
        self.assertTrue(self.ag.validateArray(percents))

    # Array should only be numbers
    def test_arrayNumbers(self):
        percents = [1, 2, 3]
        self.assertTrue(self.ag.validateArray(percents))

    # Array should not be decimals
    def test_arrayDecimals(self):
        percents = [1.5, 2.1, 3.99]
        self.assertFalse(self.ag.validateArray(percents))

    # Array should not be None
    def test_arrayNone(self):
        percents = [None, None, None]
        self.assertFalse(self.ag.validateArray(percents))

    # Array should not be Strings
    def test_arrayString(self):
        percents = ["Hello", "world", "!"]
        self.assertFalse(self.ag.validateArray(percents))

    # Array should be positive
    def test_arrayNegative(self):
        percents = [-1, -2, -3]
        self.assertFalse(self.ag.validateArray(percents))

    # Array should not have more than one data type
    def test_arrayMixed(self):
        percents = [-1, "Hello", None, 2, 4.5]
        self.assertFalse(self.ag.validateArray(percents))

#
# validPercents()
#
    # Percents should not exceed 100
    def test_percentsUpperBound(self):
        percents = [99, 100, 1]
        self.assertTrue(self.ag.validatePercents(percents))
        percents = [101, 200, 500]
        self.assertFalse(self.ag.validatePercents(percents))
    
#
# averagePercent()
#
    # Average should return the correct value
    def test_averagePercentCorrect(self):
        percents = [1, 2, 3]
        self.assertEqual(self.ag.average(percents), 2)
        percents = [2, 2, 2]
        self.assertEqual(self.ag.average(percents), 2)

    # Average should be an int
    def test_averagePercentReturnInt(self):
        percents = [1, 2, 3]
        self.assertTrue(isinstance(self.ag.average(percents), int))

    # Average should round up when > .5
    def test_averagePercentRoundUp(self):
        percents = [55, 28, 90, 70]
        self.assertEqual(self.ag.average(percents), 61)

    # Average should round up when = .5
    def test_averagePercentRoundHalf(self):
        percents = [3.5, 3.5, 3.5]
        self.assertEqual(self.ag.average(percents), 4)

    # Average should round down when < .5
    def test_averagePercentRoundDown(self):
        percents = [55, 28, 90, 70, 73]
        self.assertEqual(self.ag.average(percents), 63)

    # Average should not be more than 100
    def test_averagePercentUpper(self):
        percents = [55, 28, 90, 70, 73]
        self.assertLessEqual(self.ag.average(percents), 100)

    # Average should not be negative
    def test_averagePercentLower(self):
        percents = [55, 28, 90, 70, 73]
        self.assertGreaterEqual(self.ag.average(percents), 0)

#
# total()
#
    # Total lines should be the correct value
    def test_totalLinesCorrect(self):
        lines = [1, 2, 3]
        self.assertEqual(self.ag.sum(lines), 6)

    # Total lines should be greater than or equal to 0
    def test_totalLinesLower(self):
        lines = [1, 2, 3]
        self.assertGreaterEqual(self.ag.sum(lines), 0)

#
# populateNames()
#
    # Should return an array
    def test_returnsList(self):
        self.assertTrue(isinstance(self.names, list))

    # Should return an array of strings
    def test_returnsListStrings(self):
        for name in self.names:
            self.assertTrue(isinstance(name, str))

    # Should return an array of the correct names
    def test_returnsListNames(self):
        self.assertTrue("Matt" in self.names)
        self.assertTrue("Armen" in self.names)
        self.assertTrue("Sam" in self.names)

#
# parseData() for percents
#
    # Should return an array
    def test_returnsListPercents(self):
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Matt", "percents"), list))
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Armen", "percents"), list))
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Sam", "percents"), list))

    # Should return these values
    def test_returnsMaxPercents(self):
        # Matt
        percents = self.ag.parseData(self.results, "Matt", "percents" )
        self.assertTrue(90 in percents)
        self.assertTrue(33 in percents)

        # Armen
        percents = self.ag.parseData(self.results, "Armen", "percents")
        self.assertTrue(70 in percents)
        self.assertTrue(70 in percents)
        self.assertTrue(79 in percents)

        # Sam
        percents = self.ag.parseData(self.results, "Sam", "percents" )
        self.assertTrue(43 in percents)
        self.assertTrue(34 in percents)
        self.assertTrue(88 in percents)

    # Should return these values
    def test_lengthPercents(self):
        # Matt
        percents = self.ag.parseData(self.results, "Matt", "percents" )
        self.assertEqual(len(percents), 3)

        # Armen
        percents = self.ag.parseData(self.results, "Armen", "percents")
        self.assertEqual(len(percents), 3)

        # Sam
        percents = self.ag.parseData(self.results, "Sam", "percents" )
        self.assertEqual(len(percents), 3)

#
# parseData() for lines
#
    # Should return an array
    def test_returnsListLines(self):
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Matt", "lines"), list))
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Armen", "lines"), list))
        self.assertTrue(isinstance(self.ag.parseData(self.results, "Sam", "lines"), list))

    # Should return these values
    def test_returnsMaxLines(self):
        # Matt
        lines = self.ag.parseData(self.results, "Matt", "lines")
        self.assertTrue(77 in lines)
        self.assertTrue(45 in lines)
        self.assertTrue(100 in lines)

        # Armen
        lines = self.ag.parseData(self.results, "Armen", "lines")
        self.assertTrue(20 in lines)
        self.assertTrue(45 in lines)
        self.assertTrue(20 in lines)

        # Sam
        lines = self.ag.parseData(self.results, "Sam", "lines")
        self.assertTrue(77 in lines)
        self.assertTrue(15 in lines)
        self.assertTrue(100 in lines)

    # Should return these lengths
    def test_lengthLines(self):
        # Matt
        lines = self.ag.parseData(self.results, "Matt", "lines")
        self.assertEqual(len(lines), 3)

        # Armen
        lines = self.ag.parseData(self.results, "Armen", "lines")
        self.assertEqual(len(lines), 3)

        # Sam
        lines = self.ag.parseData(self.results, "Sam", "lines")
        self.assertEqual(len(lines), 3)

#
# sort()
#
    # Should return these results after sort
    def test_sortResults(self):
        array = []
        array.append(Aggregation("Matt", 71))
        array.append(Aggregation("Armen", 73))
        array.append(Aggregation("Sam", 55))
        array = self.ag.sort(array)

        self.assertEqual(array[0].data, 73)
        self.assertEqual(array[1].data, 71)
        self.assertEqual(array[2].data, 55)

#
# aggregateData()
#
    # Valid variable type
    def test_validResultsType(self):
        self.assertTrue(self.ag.aggregateData())

    # Invalid variable type
    def test_invalidResultsType(self):
        self.ag.results = 5
        self.assertFalse(self.ag.aggregateData())

    # Invalid None type
    def test_invalidResultsTypeNone(self):
        self.ag.results = None
        self.assertFalse(self.ag.aggregateData())

    # Too high percentage value as a string
    def test_percentTooHighAsString(self):
        self.ag.results = []
        self.ag.results.append(Result(2, "Matt", "Sam", self.validURL, "200", "101", 15))
        self.assertFalse(self.ag.aggregateData())

    # Negative percentage value as a string
    def test_negativePercentAsString(self):
        self.ag.results = []
        self.ag.results.append(Result(2, "Matt", "Sam", self.validURL, "-100", "-200", 15))
        self.assertFalse(self.ag.aggregateData())

    # Too high percentage value as an int
    def test_percentTooHighAsInt(self):
        self.ag.results = []
        self.ag.results.append(Result(2, "Matt", "Sam", self.validURL, 200, 101, 15))
        self.assertFalse(self.ag.aggregateData())

    # Negative percentage value as an int
    def test_negativePercentAsInt(self):
        self.ag.results = []
        self.ag.results.append(Result(2, "Matt", "Sam", self.validURL, -101, -101, 15))
        self.assertFalse(self.ag.aggregateData())


if __name__ == '__main__':
    unittest.main()

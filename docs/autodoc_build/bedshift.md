<script>
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('h3 code').forEach((block) => {
    hljs.highlightBlock(block);
  });
});
</script>

<style>
h3 .content { 
    padding-left: 22px;
    text-indent: -15px;
 }
h3 .hljs .content {
    padding-left: 20px;
    margin-left: 0px;
    text-indent: -15px;
    martin-bottom: 0px;
}
h4 .content, table .content, p .content, li .content { margin-left: 30px; }
h4 .content { 
    font-style: italic;
    font-size: 1em;
    margin-bottom: 0px;
}

</style>


# Package `bedshift` Documentation

## <a name="Bedshift"></a> Class `Bedshift`
The bedshift object with methods to perturb regions


```python
def __init__(self)
```

Initialize self.  See help(type(self)) for accurate signature.



```python
def add(self, df, addrate, addmean, addstdev)
```

Add regions
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb
- `addrate` (`float`):  the rate to add regions
- `addmean` (`float`):  the mean length of added regions
- `addstdev` (`float`):  the standard deviation of the length of added regions


#### Returns:

- `pandas.DataFrame`:  the new dataframe object after adds




```python
def add_from_file(self, df, fp, addrate)
```

Add regions from another bedfile to this perturbed bedfile
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb
- `addrate` (`float`):  the rate to add regions
- `fp` (`str`):  the filepath to the other bedfile




```python
def all_perturbations(self, df, addrate=0.0, addmean=320.0, addstdev=30.0, addfile=None, shiftrate=0.0, shiftmean=0.0, shiftstdev=150.0, cutrate=0.0, mergerate=0.0, droprate=0.0)
```

Perform all five perturbations in the order of add, shift, cut, merge, drop.
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb.
- `addrate` (`float`):  the rate (as a proportion of the total number of regions) to add regions
- `addmean` (`float`):  the mean length of added regions
- `addstdev` (`float`):  the standard deviation of the length of added regions
- `shiftrate` (`float`):  the rate to shift regions (both the start and end are shifted by the same amount)
- `shiftmean` (`float`):  the mean shift distance
- `shiftstdev` (`float`):  the standard deviation of the shift distance
- `cutrate` (`float`):  the rate to cut regions into two separate regions
- `mergerate` (`float`):  the rate to merge two regions into one
- `droprate` (`float`):  the rate to drop/remove regions


#### Returns:

- `pandas.DataFrame`:  the new dataframe after all perturbations




```python
def cut(self, df, cutrate)
```

Cut regions to create two new regions
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb.
- `cutrate` (`float`):  the rate to cut regions into two separate regions


#### Returns:

- `pandas.DataFrame`:  the new dataframe after cuts




```python
def drop(self, df, droprate)
```

Drop regions
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb.
- `droprate` (`float`):  the rate to drop/remove regions


#### Returns:

- `pandas.DataFrame`:  the new dataframe after drops




```python
def merge(self, df, mergerate)
```

Merge two regions into one new region
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb.
- `mergerate` (`float`):  the rate to merge two regions into one


#### Returns:

- `pandas.DataFrame`:  the new dataframe after merges




```python
def pick_random_chrom(self)
```

Utility function to pick a random chromosome
#### Returns:

- `str, float chrom_str, chrom_len`:  chromosome number and length




```python
def read_bed(self, bedfile_path)
```

Read in a bedfile to pandas DataFrame format
#### Parameters:

- `bedfile_path` (`str`):  the path to the bedfile




```python
def shift(self, df, shiftrate, shiftmean, shiftstdev)
```

Shift regions
#### Parameters:

- `df` (`pandas.DataFrame`):  the dataframe to perturb.
- `shiftrate` (`float`):  the rate to shift regions (both the start and end are shifted by the same amount)
- `shiftmean` (`float`):  the mean shift distance
- `shiftstdev` (`float`):  the standard deviation of the shift distance


#### Returns:

- `pandas.DataFrame`:  the original dataframe after shifts




```python
def write_bed(self, df, outfile_name)
```

Write a pandas dataframe back into bedfile format
#### Parameters:

- `df` (`pandas.DataFrame`):  A dataframe containing regions like a bedfile
- `outfile_name` (`str`):  The name of the output bedfile







*Version Information: `bedshift` v0.2.0, generated by `lucidoc` v0.4.2*
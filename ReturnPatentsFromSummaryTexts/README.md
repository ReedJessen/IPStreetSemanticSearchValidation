## Inputs
500 `Patent Application Number` and `Summary Text` Describing the Associated `Patent Application Number`.

# Process
1. For each `Patent Application Number`, search `https://api.ipstreet.com/v2/full_text` using its `Summary Text` as the raw text search seed.
Very broad search constraints were used.
```json
{
	"q": {
		"start_date": "1976-01-01",
		"start_date_type": "application_date",
		"end_date": "2017-03-10",
		"end_date_type": "application_date",
		"applied": "True",
		"granted": "True",
		"expired": "True",
		"max_expected_results": 500,
		"page_size": 500
	}
}
```

2. The `application_number` and its index position order from the top 10 most semantically similar results were retained.
3. The `Patent Application Number` was searched for in the array of retained `application_number` from each search. If a `Patent Application Number` was found in the array of retained `application_number`, the index position at which `Patent Application Number` was found was recorded.

For example:

If `Patent Application Number`= `14487375`	

and

`search_results` = `[13048635,	14487375,	14034805,	11940569,	14705380,	11197004,	11416875,	14840164,	11292626,	12107199]`,

this search would be scored `2` because `14487375` was found on in the 2nd index position.

Alternatively, if
`Patent Application Number`= `14316476`	

and 

`search_results` = `[11639157,	12474700,	09723222,	12392491,	12828366,	14320818,	12949434,	14322158,	12461113,	10121699]`,

this search would be scored `0` because `14316476` was not found in the top ten results.

4. Thes results were then normalized on a 100% scale and charted.



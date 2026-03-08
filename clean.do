clear all
set more off

*------------------------------*
* 0. Paths 
*------------------------------*
global ROOT "C:\Users\gao_m\Desktop\Data Mining\Mideterm Project" 
global RAW  "${ROOT}/raw"
global OUT  "${ROOT}/output"  
global INT  "${ROOT}/intermediate"

*------------------------------*
* clean data
*------------------------------*
* clean GDPperCapita
import delimited "${RAW}\GDP per capita (constant 2015USD).csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y GDPperCapita
label variable GDPperCapita "GDP per capita (constant 2015USD)"

save "${INT}/gdp.dta", replace

* clean GDP growth
import delimited "${RAW}\GDP growth.csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y GDPgrowth
label variable GDPgrowth "GDP growth(%)" 

save "${INT}/gdp_growth.dta", replace


* clean Manufacturing share

import delimited "${RAW}\Manufacturing share.csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y Manushare
label variable Manushare "Manufacturing, value added (% of GDP)" 

save "${INT}/Manushare.dta", replace

* clean trade

import delimited "${RAW}\Trade.csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y trade
label variable trade "Trade (% of GDP)" 

save "${INT}/Trade.dta", replace


* clean secondary school enrollment

import delimited "${RAW}\secondary.csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y schoolsec
label variable school "School enrollment,secondary (% gross)" 

save "${INT}/secondary.dta", replace

* clean tertiary school enrollment

import delimited "${RAW}\tertiary.csv", ///
    clear varnames(1)
	
drop indicatorname indicatorcode
	
ds v*
foreach v of varlist `r(varlist)' {
    local yr : variable label `v'
    rename `v' y`yr'
}

reshape long y, i(countryname) j(year)

rename y schoolter
label variable school "School enrollment,tertiary (% gross)" 

save "${INT}/tertiary.dta", replace

*------------------------------*
* merge data
*------------------------------*
use "${INT}/gdp.dta",clear
merge 1:1 countryname year using "${INT}/gdp_growth.dta"
drop _merge
merge 1:1 countryname year using "${INT}/Manushare.dta"
drop _merge
merge 1:1 countryname year using "${INT}/Trade.dta"
drop _merge
merge 1:1 countryname year using "${INT}/secondary.dta"
drop _merge
merge 1:1 countryname year using "${INT}/tertiary.dta"
drop _merge

export excel using "${OUT}/final_panel.xlsx", ///
firstrow(variables) replace
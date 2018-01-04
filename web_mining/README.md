# Northeastern University Course Relations

Script that queries Northeastern University's dynamic search [site](https://wl11gp.neu.edu/udcprod8/NEUCLSS.p_disp_dyn_sched) for course data, scrapes the page for courses and their associated pre/co-requisites, and outputs the result in [DOT](https://graphviz.gitlab.io/_pages/doc/info/lang.html) for Graph Visualisation with [GraphViz](https://graphviz.gitlab.io).


## Example Usage

``` bash
./courses.py --instructor "Derbinsky, Nathaniel L." "Fall 2017 Semester" > derbinsky.gv
./courses.py --subject CS --level UG "Fall 2017 Semester" > cs_undergrad.gv
./courses.py --subject CS --level GR "Fall 2017 Semester" > cs_grad.gv

dot -Tpng -oderbinsky.png derbinsky.gv
dot -Tpng -ocs_undergrad.png cs_undergrad.gv
dot -Tpng -ocs_grad.png cs_grad.gv
```
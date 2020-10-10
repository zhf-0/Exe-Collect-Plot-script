# Exe-Collect-Plot-script
scripts for executing, collecting data and plotting

## main
之前脚本的普适性不是很好，更多的是为了完成一个单独任务而写的。最近根据`fasp`中程序执行的特点，重新写了一遍，程序的重点：`class Running`有了以下改变
- 之前的程序，传递运行参数的方式太随意，不具有普适性。目前的程序统一使用`fasp`中默认支持的方式，通过`-ini input.dat`的方式指定程序运行参数。
- 类中增加了两个新的成员函数：`ParseInputConfig()`和`OutputConfig()`。顾名思义，`ParseInputConfig()`函数负责解析`input.dat`，把各种参数的名称与对应的值输入到字典中，此处的`input.dat`可以理解为一个模板文件，并不是实际运行时的参数配置文件。
- `OutputConfig()`函数负责把字典所代表的参数配置，以`fasp`支持的格式，输出到单独的文件中，该文件才是真正运行时的参数配置文件。在输出之前，可以修改字典中的参数配置，因此该函数同时负责修改和输出。

## future work

- 通过`GridSearch.py`进行网格搜索，会得到大量数据，目前只是把数据输出到普通文本文件中，再利用`plot.py`程序对文件中的文本内容进行处理，得到数据，再画图。在这一过程中，数据先是写入到文件中，再利用程序提取出数据进行画图，做了很多无用功，更重要的是，随着数据的增多，这种原始的管理方式很低效，也无法为`plot.py`提供统一的数据访问接口。综上，目前考虑使用`Python`中内置的数据库`sqlite3`管理数据，对`GridSearch.py`进行修改，但是不会改变`class Running`的内容。

import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import h5py
import glob
import io
# plt.rcdefaults()

class RbYbJupyter(object):
    def __init__(self):
        self.plot_kwargs = {
            # 'fmt':'o-',
            # 'color': seaborn.color_palette()[0],
            'markeredgewidth': 1,
            'markeredgecolor': 'black',
            'ecolor': 'grey',
            'capsize': 2.5,
            'capthick': 1
        }
        self.footer_pos = 0.0
        self.header_pos = 1.0
        self.pad = 2

    def init_paths(self,base_path):
        self._base_path = base_path
        if self._base_path[-1] != '/':
            self._base_path += '/'
        self._date_seq_str = self._date.replace('/','-') + ': ' + self._seq_name
    
    def add_figure_to_clipboard(self, fig):
        caption = 'test caption'
        buffer = io.BytesIO()
        fig.savefig(buffer)
        data_to_clipboard = QMimeData() 
        data_to_clipboard.setImageData(QImage.fromData(buffer.getvalue()))
        data_to_clipboard.setText(caption)
        self.clipboard = self.app.clipboard()
        self.clipboard.clear(mode=self.clipboard.Clipboard)
        self.clipboard.setText('test')
    
    def generate_metadata(self, scans, df, globals_list):
        metadata_string = self._date_seq_str.replace(': ','_') + ' // seq: ' + str(scans) + ' // '
        for var in globals_list:
            value_string = str(df[var].values[0,0])
            metadata_string += var + ': '+ value_string + ', '
        metadata_string = metadata_string[:-2]
        return metadata_string

    def get_scans(self):
        """
        Returns the paths of all the scan folders in the day's base path.
        """
        full_paths = glob.glob(self._base_path+'/*')
        return full_paths
    
    def scan_str(self, scans):
        """
        Generates the string to annotate plots with sequence numbers.
        """
        scan_string = str(scans)
        scan_str_list = list(scan_string)
        j = 0
        for idx,val in enumerate(scan_str_list):
            if idx % 75 == 0 and idx != 0:
                last_comma_idx = scan_string[:idx].rfind(',')
                scan_str_list.insert(last_comma_idx+1 + j,'\n')
                scan_string = ''.join(scan_str_list[:last_comma_idx+1]) + scan_string[last_comma_idx+1:]
                j += 1
        return ''.join(scan_str_list)

    def get_runs(self,scans):
        runs = []
        for scan in scans:
            scan_string = '{scan:0>4}'.format(scan = scan)
            runs += glob.glob(self._base_path + scan_string +'/*.h5')
        print(runs)
        return runs


    def get_dataframes(self,scans,verbose=False,run_info=False):
        files = self.get_runs(scans)
        data_dict = {}
        for _file in files:
                _dict = {}
                path = _file
                try:
                    with h5py.File(path,'r') as f:
                        for group in f['results']:
                            for attr in f['results'][group].attrs:
                                _dict["{}__{}".format(group,attr)] = float(f['results'][group].attrs[attr])

                        for attr in f['globals'].attrs:
                            try:
                                _dict[attr] = float(f['globals'].attrs[attr])
                            except:
                                _dict[attr] = f['globals'].attrs[attr]

                        if run_info:
                            for attr in f.attrs:
                                _dict[attr] = f.attrs[attr]

                    data_dict[_file] = _dict
                except:
                    if verbose:
                        print(" no {}".format(path))
                    else:
                        pass
        return pd.DataFrame(data_dict).transpose()

    def get_dataframe_multi_scan(self,scans):
        return self.get_dataframes(scans)
    
    def get_averaged_dataframe(self, scans, var_list, **kwargs):
        """get averaged dataframe for names with args as all arguments
        # todo make these ind go away by finding actual values, until then set it
        to high
        """
        df = self.get_dataframe_multi_scan(scans)
        return df.groupby(var_list).agg([np.mean, np.std, np.var])

    def _plot_1d(self, scans, var_list, plot_var_list, metadata_var_list, fit_line=False, fit_gauss=False, fmt='o-', *args,**kwargs):
        df = self.get_averaged_dataframe(scans, var_list)
        fig, ax = plt.subplots(len(plot_var_list), 1, *args,**kwargs)
        x = np.array(df.index)
        if len(plot_var_list) < 2:
            _var = plot_var_list[0]
            ax.errorbar(x, df[_var,'mean'].values,
                           yerr= df[_var, 'std'].values,
                           fmt=fmt,
                           markeredgewidth=1,
                           markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1)
            if fit_gauss:
                mod = GaussianModel() + ConstantModel()
                yy = df[_var, 'mean'].values
                sig = np.mean(x)/10
                if sig < .05:
                    sig = 1

                pars = mod.make_params(amplitude=np.max(yy),
                                       center=np.mean(x),
                                       sigma=sig,
                                       c=0)
                res = mod.fit(x=x, data=yy, params=pars)
                xx = np.linspace(np.min(x), np.max(x), 1000)
                ax.plot(xx,res.eval(x=xx))
                print(res.fit_report())
            if fit_line:
                mod = LinearModel()
                yy = df[_var, 'mean'].values
                pars = mod.make_params(slope=1,
                                      intercept=0)
                res = mod.fit(x=x, data=yy, params=pars)
                xx = np.linspace(np.min(x), np.max(x), 1000)
                ax.plot(xx,res.eval(x=xx))
                print(res.fit_report())

        else:
            for i, _var in enumerate(plot_var_list):
                ax[i].errorbar(x, df[_var,'mean'].values,
                               yerr= df[_var, 'std'].values,
                               fmt=fmt,
                               markeredgewidth=1,
                               markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1)
        if len(plot_var_list) < 2:
            ax.set_xlabel(var_list[0])
            ax.grid()
        else:
            for i in range(len(plot_var_list)):
                ax[i].set_xlabel(var_list[0])
                ax[i].title(plot_var_list[i])
                ax[i].grid()
        scan_str_art = fig.text(0,self.footer_pos, 'seq: ' + self.scan_str(scans), horizontalalignment='left',verticalalignment='bottom')
        seq_str_art = fig.text(0,self.header_pos, self._date_seq_str, horizontalalignment='left',verticalalignment='top')
        scan_str_art.set_in_layout(True)
        seq_str_art.set_in_layout(True)
        fig.tight_layout(pad=self.pad)
        metadata = self.generate_metadata(scans, df, metadata_var_list)
        return metadata, fig


    def _plot_2d(self, scans, var_list, plot_var_list, metadata_var_list, fmt='o-', reverse=False, *args, **kwargs):
        if reverse:
            var_list = list(reversed(var_list))

        df = self.get_averaged_dataframe(scans, var_list)
        n_vars = len(df.index.unique().levels[1])
        if n_vars > 6:
            pal = seaborn.color_palette('husl', n_vars)
        else:
            pal = seaborn.color_palette()
        df = df.reset_index()
        fig, ax = plt.subplots(len(plot_var_list), 1, *args, **kwargs)
        for ii, (value, df1) in enumerate(df.groupby(var_list[1])):
            x = df1[var_list[0]]
            if len(plot_var_list) < 2:
                _var = plot_var_list[0]
                ax.errorbar(x, df1[_var,'mean'].values,
                               yerr= df1[_var, 'std'].values,
                               fmt=fmt,
                               color = pal[ii],
                               markeredgewidth=1,
                               markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1,
                               label="{}_{}".format(var_list[1], value))

            else:
                for i, _var in enumerate(plot_var_list):
                    ax[i].errorbar(x, df1[_var,'mean'].values,
                                   yerr= df1[_var, 'std'].values,
                                   fmt=fmt,
                                   color = pal[ii],
                                   markeredgewidth=1,
                                   markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1,
                                   label="{}_{}".format(var_list[1], value))
                    
        if len(plot_var_list) < 2:
            ax.legend()
            ax.set_xlabel(var_list[0])
            ax.grid()
        else:
            for i in range(len(plot_var_list)):
                ax[i].legend()
                ax[i].grid()
                ax[i].set_xlabel(var_list[0])
                ax[i].set_title(plot_var_list[i])
        scan_str_art = fig.text(0,self.footer_pos, 'seq: ' + self.scan_str(scans), horizontalalignment='left',verticalalignment='bottom')
        seq_str_art = fig.text(0,self.header_pos, self._date_seq_str, horizontalalignment='left',verticalalignment='top')
        scan_str_art.set_in_layout(True)
        seq_str_art.set_in_layout(True)
        fig.tight_layout(pad=self.pad)
        metadata = self.generate_metadata(scans, df, metadata_var_list)
        return metadata, fig

    def plot_2d_together(self, scans, var_list, plot_var_list, metadata_var_list, fmt='o-', reverse=False, *args, **kwargs):
        if reverse:
            var_list = list(reversed(var_list))

        df = self.get_averaged_dataframe(scans, var_list)
        n_vars = len(df.index.unique().levels[1])
        if n_vars > 6:
            pal = seaborn.color_palette('husl', n_vars)
        else:
            pal = seaborn.color_palette()
        df = df.reset_index()
        fig, ax = plt.subplots(len(plot_var_list), 1, *args, **kwargs)
        for ii, (value, df1) in enumerate(df.groupby(var_list[1])):
            x = df1[var_list[0]]
            if len(plot_var_list) < 2:
                _var = plot_var_list[0]
                ax.errorbar(x, df1[_var,'mean'].values,
                               yerr= df1[_var, 'std'].values,
                               fmt=fmt,
                               color = pal[ii],
                               markeredgewidth=1,
                               markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1,
                               label="{}_{}".format(var_list[1], value))


            else:
                for i, _var in enumerate(plot_var_list):
                    ax.errorbar(x, df1[_var,'mean'].values,
                                   yerr= df1[_var, 'std'].values,
                                   fmt=fmt,
                                   color = pal[ii],
                                   markeredgewidth=1,
                                   markeredgecolor='black', ecolor='grey',capsize=2.5,capthick=1,
                                   label="{}_{}".format(var_list[1], value))
        if len(plot_var_list) < 2:
            ax.legend()
            ax.set_xlabel(var_list[0])
        else:
            # for i in range(len(plot_var_list)):
            ax.legend()
            ax.set_xlabel(var_list[0])
            ax.set_title(plot_var_list[i])
        ax.grid()
        scan_str_art = fig.text(0,self.footer_pos, 'seq: ' + self.scan_str(scans), horizontalalignment='left',verticalalignment='bottom')
        seq_str_art = fig.text(0,self.header_pos, self._date_seq_str, horizontalalignment='left',verticalalignment='top')
        scan_str_art.set_in_layout(True)
        seq_str_art.set_in_layout(True)
        fig.tight_layout(pad=self.pad)
        metadata = self.generate_metadata(scans, df, metadata_var_list)
        return metadata, fig

    
    def _plot_3d(self, scans, var_list, plot_var_list, metadata_var_list, *args, **kwargs):
        df = self.get_averaged_dataframe(scans, var_list)
        df = df.reset_index()
        for _var in plot_var_list:
            _x = df[(var_list[0])].values
            _y = df[(var_list[1])].values
            _z = df[(var_list[2])].values
            _c = df[_var, 'mean'].values
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection = '3d')
            a = ax.scatter(_x,_y,_z,c=_c, cmap=plt.cm.viridis,s=40)
            ax.set_xlabel(var_list[0])
            ax.set_ylabel(var_list[1])
            ax.set_zlabel(var_list[2])
            plt.colorbar(a)
        metadata = self.generate_metadata(scans, df, metadata_var_list)
        return metadata, fig
        

    def plot(self, scans, var_list, plot_var_list, metadata_var_list, *args, **kwargs):
        if len(var_list) < 2:
            return self._plot_1d(scans, var_list, plot_var_list, metadata_var_list, *args, **kwargs)
        elif len(var_list) == 2:
            return self._plot_2d(scans, var_list, plot_var_list, metadata_var_list, *args, **kwargs)
        else:
            return self._plot_3d(scans, var_list, plot_var_list, metadata_var_list, *args, **kwargs)

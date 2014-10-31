pro allan_v2

!path='/home/jenna/goddard/pro:'+!path

;head_only=mrdfits('OTF20000_1501.fits', 1, header)
;print, header
;obs_time=0.35 ;seconds
;dead_time=0.05
tau=0.4
T_arr=indgen(1501)*tau
tau_arr=indgen(601)*tau
;tau_arr=indgen(501)*tau
    

totpow=fltarr(n_elements(T_arr),64)

for i=0, 1500 do begin
	readcol, 'total_power_'+strcompress(i,/remove_all)+'.dat', /silent, $
	skipline=2, row, row1, row2, row3, row4, row5, row6, row7, row8
	totpow[i,*]=[row1, row2, row3, row4, row5, row6, row7, row8]
endfor

sig_tau2=fltarr(64, n_elements(tau_arr)-1)
for i=0, 63 do begin
	sig_tau2[i,*]=avar(totpow[*,i], tau, tau_arr)
;	remove, 175, sig_tau2[i,*]
;	remove, 349, sig_tau2[i,*]
;	remove, 349, sig_tau2[i,*]
;	remove, 349, sig_tau2[i,*]
endfor

;remove, 175, tau_arr
;remove, 349, tau_arr
;remove, 349, tau_arr
;remove, 349, tau_arr

sig_tau2_reverse=reverse(sig_tau2)
sig_tau2_plot=fltarr(8,8,n_elements(sig_tau2[0,*]))
for i=0, 7 do begin
	for j=0, 7 do begin
;		print, (7-j)+8*i
		single=sig_tau2_reverse[(7-j)+8*i,*]
		sig_tau2_plot[i,j,*]=single
;		print, n_elements(sig_tau2[(7-j)+8*i,*])
	endfor
endfor

;set_plot, 'ps'
;device, /landscape, /color
;LOADCT, 5
xtick_names=['0.1', '1', '10', '100', '1000']

print, "I'm working 0 ...."
!p.multi=[0,8,8]
for i=0, 7 do begin
	for j=0, 7 do begin
	if (i eq 7) and (j eq 0) then begin
	plot, tau_arr, sig_tau2_plot[i,j,*], $
		/xlog, /ylog, xrange=[10^(-1.), 10^3.], $
		yrange=[10.^(-8), 10.^(-2)], xtickname=xtick_names, $
		xmargin=[0,0], ymargin=[0,0], xstyle=1, ystyle=1, $
		charsize=1.5, charthick=3, thick=3, color=255, $
		xtitle='Time (s)', ytitle='Normalized Allan Variance'
	endif else begin
	plot, tau_arr, sig_tau2_plot[i,j,*], $
		/xlog, /ylog, xrange=[10.^(-1), 10.^3], $
		yrange=[10.^(-8), 10.^(-2)], $
		xmargin=[0,0], ymargin=[0,0], xstyle=1, ystyle=1, $
		charsize=1.d-6, thick=3, color=255
	print, "I'm stilloworking", i, j
	endelse
	endfor
endfor

;device, /close

end

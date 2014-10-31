function avar, totpow, tau, tau_arr

sig_tau2=fltarr(n_elements(tau_arr)-1)
for i=1, n_elements(tau_arr)-1 do begin
	M_x  = n_elements(totpow[*])
	norm = max(totpow[*]) ;normalization factor
	x_l  = totpow[0:M_x-2*i-1]/norm
	x_m  = totpow[i:M_x-i-1]/norm
	x_u  = totpow[2*i:M_x-1]/norm
;	print, i, n_elements(x_l), n_elements(x_m), n_elements(x_u)
	coeff = 1./(2*(i*tau)^2*(n_elements(x_l)-2*i))
	y2 = (x_u - 2*x_m + x_l)^2
	sum = total(y2)
	sig_tau2[i-1] = coeff*sum
endfor

return, sig_tau2
end

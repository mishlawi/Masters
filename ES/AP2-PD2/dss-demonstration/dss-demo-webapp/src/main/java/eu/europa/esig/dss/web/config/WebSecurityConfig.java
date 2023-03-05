package eu.europa.esig.dss.web.config;

import eu.europa.esig.dss.utils.Utils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.header.HeaderWriter;
import org.springframework.security.web.header.writers.DelegatingRequestMatcherHeaderWriter;
import org.springframework.security.web.header.writers.StaticHeadersWriter;
import org.springframework.security.web.header.writers.frameoptions.XFrameOptionsHeaderWriter;
import org.springframework.security.web.header.writers.frameoptions.XFrameOptionsHeaderWriter.XFrameOptionsMode;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.handler.MappedInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Collection;

@Configuration
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

	@Value("${web.security.cookie.samesite}")
	private String samesite;

	@Value("${web.security.csp}")
	private String csp;

	/** API urls (REST/SOAP webServices) */
	private static final String[] API_URLS = new String[] {
			"/services/rest/**", "/services/soap/**"
	};

	private DriverManagerDataSource dataSource;

	@Override
	protected void configure(HttpSecurity http) throws Exception {
		// javadoc uses frames
		http.authorizeRequests()
			.antMatchers("/css/**","/images/**","/fonts/**","/webjars/**").permitAll()
			.antMatchers( "/signup", "/signup_process").permitAll()
			.anyRequest().authenticated()
			.and()
			.formLogin()
			.loginPage("/login")
			.defaultSuccessUrl("/user-profile",true)
			.permitAll()
			.and()
			.logout()
			.logoutSuccessUrl("/login")
			.permitAll()
			.and()
			.csrf()
			.disable();

		http.headers().addHeaderWriter(javadocHeaderWriter());
		http.headers().addHeaderWriter(svgHeaderWriter());
		http.headers().addHeaderWriter(serverEsigDSS());

		http.csrf().ignoringAntMatchers(API_URLS); // disable CSRF for API calls (REST/SOAP webServices)

		if (Utils.isStringNotEmpty(csp)) {
			http.headers().contentSecurityPolicy(csp);
		}
	}

	//	@Autowired
//	public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
//		auth
//				.inMemoryAuthentication()
//				.withUser("user@gmail.com").password(passwordEncoder().encode("pass")).roles("USER");
//	}
//
	@Autowired
	public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
		DriverManagerDataSource dataSourceBuilder = new DriverManagerDataSource();
		dataSourceBuilder.setDriverClassName("com.mysql.jdbc.Driver");
		dataSourceBuilder.setUrl("jdbc:mysql://localhost:3306/pd2?serverTimezone=UTC&useSSL=false");
		dataSourceBuilder.setUsername("root");
		dataSourceBuilder.setPassword("root");

		this.dataSource = dataSourceBuilder;
		auth.jdbcAuthentication()
				.dataSource(dataSource)
				.usersByUsernameQuery("select username,password,1 from users where username = ?")
				.passwordEncoder(passwordEncoder())
				.authoritiesByUsernameQuery("select username,'ROLE_USER' from users where username = ?");



	}

	@Bean
	public PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}

	@Bean
	public HeaderWriter javadocHeaderWriter() {
		final AntPathRequestMatcher javadocAntPathRequestMatcher = new AntPathRequestMatcher("/apidocs/**");
		final HeaderWriter hw = new XFrameOptionsHeaderWriter(XFrameOptionsMode.SAMEORIGIN);
		return new DelegatingRequestMatcherHeaderWriter(javadocAntPathRequestMatcher, hw);
	}

	@Bean
	public  HeaderWriter svgHeaderWriter() {
		final AntPathRequestMatcher javadocAntPathRequestMatcher = new AntPathRequestMatcher("/validation/diag-data.svg");
		final HeaderWriter hw = new XFrameOptionsHeaderWriter(XFrameOptionsMode.SAMEORIGIN);
		return new DelegatingRequestMatcherHeaderWriter(javadocAntPathRequestMatcher, hw);
	}

	@Bean
	public HeaderWriter serverEsigDSS() {
		return new StaticHeadersWriter("Server", "ESIG-DSS");
	}

	@Bean
	public MappedInterceptor cookiesInterceptor() {
		return new MappedInterceptor(null, new CookiesHandlerInterceptor());
	}

	/**
	 * The class is used to enrich "Set-Cookie" header with "SameSite=strict" value
	 *
	 * NOTE: Spring does not provide support of cookies handling out of the box
	 *       and requires a Spring Session dependency for that.
	 *       Here is a manual way of response headers configuration
	 */
	private final class CookiesHandlerInterceptor implements HandlerInterceptor {

		/** The "SameSite" cookie parameter name */
		private static final String SAMESITE_NAME = "SameSite";

		@Override
		public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
							   ModelAndView modelAndView) {
			if (Utils.isStringNotEmpty(samesite)) {
				Collection<String> setCookieHeaders = response.getHeaders(HttpHeaders.SET_COOKIE);
				if (Utils.isCollectionNotEmpty(setCookieHeaders)) {
					for (String header : setCookieHeaders) {
						header = String.format("%s; %s=%s", header, SAMESITE_NAME, samesite);
						response.setHeader(HttpHeaders.SET_COOKIE, header);
					}
				}
			}
		}
	}

}

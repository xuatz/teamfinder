import React, { Component } from 'react'
import { Helmet } from 'react-helmet'

import Alert from 'react-s-alert';
import { Grid } from 'react-bootstrap'
import TopNav from 'components/layout/TopNav'
import Footer from 'components/layout/Footer'
import FeedbackButton from 'containers/feedback/FeedbackButton'
import FeedbackModal from 'containers/feedback/FeedbackModal'

class Base extends Component {

    render() {
        return (
            <div id='page-wrapper'>
                <Helmet>
                    <title>Dota 2 Team Finder</title>
                    <meta name="description" content="Find your next Dota 2 team!" />
                </Helmet>

                <TopNav loggedIn={false} location={this.props.location.pathname}/>

                <div id='page-content'>
                    <Grid>
                        {this.props.children}
                    </Grid>
                </div>

                <Footer />
                <Alert stack={{limit: 3}} effect='slide' />
                <FeedbackButton />
                <FeedbackModal />
            </div>
        )
    }

}
export default Base

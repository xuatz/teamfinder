import React, { Component } from 'react'
import { connect } from 'react-redux'
import { requestTeam } from 'actions/teams'
import { teamsSelector } from 'utils/selectors'

export const _withTeam = teamId => (WrappedComponent) => {

    class WithTeam extends Component {

        componentDidMount() {
            this.props.onLoad(teamId)
        }

        render() {
            const { teams } = this.props
            const team = teams[teamId] || {}

            return <WrappedComponent team={team} {...this.props} />
        }

    }
    WithTeam = connect(
        teamsSelector,
        { onLoad: requestTeam }
    )(WithTeam)
    return WithTeam
}

export const withTeam = mapPropsToId => WrappedComponent => {

    class WithTeam extends Component {

        render() {
            const ConnectedComponent = _withTeam(mapPropsToId(this.props))(WrappedComponent)
            return <ConnectedComponent {...this.props} />
        }
    }

    return WithTeam

}

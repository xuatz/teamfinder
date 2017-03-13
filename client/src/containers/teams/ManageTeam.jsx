import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
// import { createStructuredSelector } from 'reselect'
// import { requestTeam } from 'actions/teams'

import { Link } from 'react-router'
// import { Label } from 'react-bootstrap'
import { Alert, Button, ButtonToolbar, Modal, Table } from 'react-bootstrap'
import requireAuthentication from 'components/auth/AuthenticationRequired'
import { withAllFixtures } from 'components/connectors/WithFixtures'
import { withPlayer } from 'components/connectors/WithPlayer'
import { withTeam } from 'components/connectors/WithTeam'
import TeamMemberPosition from 'components/forms/TeamMemberPosition'
// import { requestPlayer } from 'actions/playerSearch'
import { cancelDeleteTeam, tryDeleteTeam, deleteTeam, cancelDeleteTeamMember, tryDeleteTeamMember,
    deleteTeamMember, tryPromoteToCaptain, cancelPromoteToCaptain, promoteToCaptain } from 'actions/teams'
// import { playerSearchSelector } from 'utils/selectors'
import { Loading, playerIsCaptain } from 'utils'
// import { CaptainIcon, RegionIcon, PlayersIcon, PositionIcon, SkillBracketIcon } from 'utils/components/icons'

const canEditTeam = (player, team) => (
    playerIsCaptain(player, team)
)

const canRemoveTeamMember = (player, team, member) => (
    // TODO: playerIsCaptain(player, team)
    playerIsCaptain(player, team) && team.captain !== member.player.id && team.team_members.length > 1
)

const canBePromotedToCaptain = (player, team, member) => (
    playerIsCaptain(player, team) && team.captain !== member.player.id
)

class ManageTeam extends Component {

    static propTypes = {
        team: PropTypes.object.isRequired
    }

    constructor(props) {
        super(props)
        this.handleDeleteTeamClick = this.handleDeleteTeamClick.bind(this)
        this.handleDeleteTeamConfirmClick = this.handleDeleteTeamConfirmClick.bind(this)
        this.handleDeleteTeamCancelClick = this.handleDeleteTeamCancelClick.bind(this)
        this.handleDeleteTeamMemberClick = this.handleDeleteTeamMemberClick.bind(this)
        this.handleDeleteTeamMemberConfirmClick = this.handleDeleteTeamMemberConfirmClick.bind(this)
        this.handleDeleteTeamMemberCancelClick = this.handleDeleteTeamMemberCancelClick.bind(this)
        
    }

    handleDeleteTeamClick() {
        const { tryDeleteTeam, team: { team: { id } } } = this.props
        tryDeleteTeam(id)
    }

    handleDeleteTeamConfirmClick() {
        const { deleteTeam, team: { team: { id } } } = this.props
        deleteTeam(id)
    }

    handleDeleteTeamCancelClick() {
        const { cancelDeleteTeam, team: { team: { id } } } = this.props
        cancelDeleteTeam(id)
    }

    handleDeleteTeamMemberClick(teamMemberId) {
        const { tryDeleteTeamMember, team: { team: { id } } } = this.props
        tryDeleteTeamMember({ teamMemberId, teamId: id })
    }

    handleDeleteTeamMemberConfirmClick(teamMemberId) {
        const { deleteTeamMember, team: { team: { id } } } = this.props
        deleteTeamMember(teamMemberId, id)
    }

    handleDeleteTeamMemberCancelClick() {
        const { cancelDeleteTeamMember, team: { team: { id } } } = this.props
        cancelDeleteTeamMember({ teamId: id })
    }

    handlePromoteToCaptainClick(teamMemberId) {
        const { tryPromoteToCaptain, team: { team: { id } } } = this.props
        tryPromoteToCaptain({ teamMemberId, teamId: id })
    }

    handlePromoteToCaptainConfirmClick(teamMemberId) {
        const { promoteToCaptain, team: { team: { id } } } = this.props
        promoteToCaptain(teamMemberId, id)
    }

    handlePromoteToCaptainCancelClick() {
        const { cancelPromoteToCaptain, team: { team: { id } } } = this.props
        cancelPromoteToCaptain({ teamId: id })
    }

    renderDeleteTeamConfirmModal() {
        const { team: { confirmDelete, team } } = this.props
        return (
            <Modal show={confirmDelete}>
                <Modal.Header>
                    <Modal.Title>Confirm Delete Team</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <p>Are you sure you want to delete <strong>{team.name}</strong>? This cannot be undone.</p>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle='link' onClick={this.handleDeleteTeamCancelClick}>Cancel</Button>
                    <Button bsStyle='danger' onClick={this.handleDeleteTeamConfirmClick}>Delete</Button>
                </Modal.Footer>
            </Modal>
        )
    }

    renderDeleteTeamMemberConfirmModal(teamMemberId) {
        const { team: { confirmDeleteTeamMember, deleteTeamMemberError, team } } = this.props
        const teamMember = team.team_members.find(member => member.id === teamMemberId)
        return (
            <Modal show={confirmDeleteTeamMember === teamMemberId}>
                <Modal.Header>
                    <Modal.Title>Confirm Remove Team Member</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {deleteTeamMemberError && (
                        <Alert bsStyle='danger'>
                            {deleteTeamMemberError}
                        </Alert>
                    )}
                    <p>
                        Are you sure you want to remove <strong>
                        {teamMember.player.username}
                        </strong> from <strong>{team.name}</strong>? This
                        cannot be undone.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle='link'
                            onClick={() => this.handleDeleteTeamMemberCancelClick(teamMemberId)}>Cancel</Button>
                    <Button bsStyle='danger'
                            onClick={() => this.handleDeleteTeamMemberConfirmClick(teamMemberId)}>
                        Remove
                    </Button>
                </Modal.Footer>
            </Modal>
        )
    }

    renderPromoteToCaptainConfirmModal(teamMemberId) {
        const { team: { confirmPromoteToCaptain, confirmPromoteToCaptainError, team } } = this.props
        const teamMember = team.team_members.find(member => member.id === teamMemberId)
        return (
            <Modal show={confirmPromoteToCaptain === teamMemberId}>
                <Modal.Header>
                    <Modal.Title>Confirm Promote to Captain</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {confirmPromoteToCaptainError && (
                        <Alert bsStyle='danger'>
                            {confirmPromoteToCaptainError}
                        </Alert>
                    )}
                    <p>
                        Are you sure you want to promote <strong>
                        {teamMember.player.username}
                        </strong> to be the captain of <strong>{team.name}</strong>? You will no longer be able to
                        make changes to this team. This cannot be undone.
                    </p>
                </Modal.Body>
                <Modal.Footer>
                    <Button bsStyle='link'
                            onClick={() => this.handlePromoteToCaptainCancelClick(teamMemberId)}>Cancel</Button>
                    <Button bsStyle='warning'
                            onClick={() => this.handlePromoteToCaptainConfirmClick(teamMemberId)}>
                        Promote to Captain
                    </Button>
                </Modal.Footer>
            </Modal>
        )
    }

    renderTeamMemberRow(teamMember) {
        const { team: { team }, player,
            fixtures: { positions }
        } = this.props
        return (
            <tr key={teamMember.id}>
                {this.renderDeleteTeamMemberConfirmModal(teamMember.id)}
                {this.renderPromoteToCaptainConfirmModal(teamMember.id)}
                <td>
                    {teamMember.player.username}&nbsp;
                    (<Link to={`/players/${teamMember.player.id}/`}>
                        profile
                    </Link>)
                </td>
                <td>
                    <TeamMemberPosition form={`position-${teamMember.id}`} initialValues={{ position: teamMember.position }} />
                </td>
                <td>
                    <ButtonToolbar>
                        {canRemoveTeamMember(player, team, teamMember) && (
                            <Button bsSize='xs' bsStyle='danger'
                                    onClick={() => this.handleDeleteTeamMemberClick(teamMember.id)}>
                                Remove
                            </Button>
                        )}
                        {canBePromotedToCaptain(player, team, teamMember) && (
                            <Button bsSize='xs'
                                    onClick={() => this.handlePromoteToCaptainClick(teamMember.id)}>
                                Promote to Captain
                            </Button>
                        )}
                    </ButtonToolbar>
                </td>
            </tr>
        )
    }

    render() {
        const { team: { team, isLoading, lastUpdated }, player } = this.props
        return (
            <div>
                {isLoading ? <Loading /> : (
                    lastUpdated ? (
                        <div>
                            {this.renderDeleteTeamConfirmModal()}
                            <h1>
                                Manage Team: {team.name}&nbsp;
                                <span className='pull-right'>
                                    {canEditTeam(player, team) && (
                                        <Button bsStyle='danger' bsSize='sm' onClick={this.handleDeleteTeamClick}>
                                            <i className='fa fa-trash'/>&nbsp;Delete
                                        </Button>
                                    )}
                                </span>
                            </h1>
                            <h2>Players</h2>
                            <div>
                                <Table>
                                    <thead>
                                        <tr>
                                            <th>Player</th>
                                            <th>Position</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {team.team_members.map(teamMember => (
                                            this.renderTeamMemberRow(teamMember)
                                        ))}
                                    </tbody>
                                </Table>

                            </div>
                        </div>
                    ) : (
                        <div>Error retrieving team.</div>
                    )
                )}
            </div>
        )
    }
}

ManageTeam = withAllFixtures(ManageTeam)
ManageTeam = withPlayer(ManageTeam)
ManageTeam = withTeam(props => props.params.id)(ManageTeam)
ManageTeam = requireAuthentication(ManageTeam)
ManageTeam = connect(
    null,
    {
        cancelDeleteTeam,
        deleteTeam,
        tryDeleteTeam,
        cancelDeleteTeamMember,
        deleteTeamMember,
        tryDeleteTeamMember,
        tryPromoteToCaptain,
        cancelPromoteToCaptain,
        promoteToCaptain
    }
)(ManageTeam)

export default ManageTeam